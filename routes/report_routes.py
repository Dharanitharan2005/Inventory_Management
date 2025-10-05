from flask import Blueprint, render_template, request, send_file
from extensions import mongo
import pandas as pd
import io

report_bp = Blueprint('report_routes', __name__)

@report_bp.route('/balance')
def balance_report():
    pipeline = [
        {
            '$facet': {
                'inbound': [
                    {'$match': {'to_location': {'$ne': None}}},
                    {'$group': {
                        '_id': {'product': '$product_id', 'location': '$to_location'},
                        'total_in': {'$sum': '$qty'}
                    }}
                ],
                'outbound': [
                    {'$match': {'from_location': {'$ne': None}}},
                    {'$group': {
                        '_id': {'product': '$product_id', 'location': '$from_location'},
                        'total_out': {'$sum': '$qty'}
                    }}
                ]
            }
        },
        {
            '$project': {
                'all_movements': {
                    '$concatArrays': ['$inbound', '$outbound']
                }
            }
        },
        {'$unwind': '$all_movements'},
        {
            '$group': {
                '_id': '$all_movements._id',
                'total_in': {'$sum': {'$ifNull': ['$all_movements.total_in', 0]}},
                'total_out': {'$sum': {'$ifNull': ['$all_movements.total_out', 0]}}
            }
        },
        {
            '$project': {
                'product_id': '$_id.product',
                'location_id': '$_id.location',
                'balance': {'$subtract': ['$total_in', '$total_out']},
                '_id': 0
            }
        },
        {
            '$lookup': {
                'from': 'products',
                'localField': 'product_id',
                'foreignField': '_id',
                'as': 'product_info'
            }
        },
        {
            '$lookup': {
                'from': 'locations',
                'localField': 'location_id',
                'foreignField': '_id',
                'as': 'location_info'
            }
        },
        {'$unwind': '$product_info'},
        {'$unwind': '$location_info'},
        {
            '$project': {
                'product_name': '$product_info.product_name',
                'location_name': '$location_info.location_name',
                'quantity': '$balance'
            }
        },
        {'$sort': {'product_name': 1, 'location_name': 1}}
    ]

    balance_data = list(mongo.db.movements.aggregate(pipeline))

    if request.args.get('export') == 'excel':
        df = pd.DataFrame(balance_data)
        if not df.empty:
            df = df.rename(columns={
                'product_name': 'Product Name',
                'location_name': 'Location',
                'quantity': 'Quantity'
            })

        output = io.BytesIO()
        # Use the 'xlsxwriter' engine for better formatting options if needed
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Stock Balance')
            # Auto-adjust column widths
            for column in df:
                column_length = max(df[column].astype(str).map(len).max(), len(column))
                col_idx = df.columns.get_loc(column)
                writer.sheets['Stock Balance'].column_dimensions[chr(65 + col_idx)].width = column_length + 2

        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='stock_balance_report.xlsx'
        )

    return render_template('reports/balance.html', balance_data=balance_data)
