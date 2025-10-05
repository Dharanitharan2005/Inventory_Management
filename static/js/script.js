// LocalStorage keys
const PRODUCT_KEY = "products";
const LOCATION_KEY = "locations";
const MOVEMENT_KEY = "movements";

// Load existing data or initialize
let products = JSON.parse(localStorage.getItem(PRODUCT_KEY)) || [];
let locations = JSON.parse(localStorage.getItem(LOCATION_KEY)) || [];
let movements = JSON.parse(localStorage.getItem(MOVEMENT_KEY)) || [];

// DOM elements
const productForm = document.getElementById("productForm");
const productTable = document.querySelector("#productTable tbody");
const locationForm = document.getElementById("locationForm");
const locationTable = document.querySelector("#locationTable tbody");
const movementForm = document.getElementById("movementForm");
const movementTable = document.querySelector("#movementTable tbody");
const reportTable = document.querySelector("#reportTable tbody");
const generateReportBtn = document.getElementById("generateReportBtn");

const movementProduct = document.getElementById("movementProduct");
const fromLocation = document.getElementById("fromLocation");
const toLocation = document.getElementById("toLocation");

// Render functions
function renderProducts() {
  productTable.innerHTML = "";
  movementProduct.innerHTML = "<option value=''>-- Select Product --</option>";
  products.forEach(p => {
    productTable.innerHTML += `<tr><td>${p.id}</td><td>${p.name}</td></tr>`;
    movementProduct.innerHTML += `<option value="${p.id}">${p.name}</option>`;
  });
}

function renderLocations() {
  locationTable.innerHTML = "";
  fromLocation.innerHTML = "<option value=''>-- From --</option>";
  toLocation.innerHTML = "<option value=''>-- To --</option>";
  locations.forEach(l => {
    locationTable.innerHTML += `<tr><td>${l.id}</td><td>${l.name}</td></tr>`;
    fromLocation.innerHTML += `<option value="${l.id}">${l.name}</option>`;
    toLocation.innerHTML += `<option value="${l.id}">${l.name}</option>`;
  });
}

function renderMovements() {
  movementTable.innerHTML = "";
  movements.forEach(m => {
    const prod = products.find(p => p.id === m.productId)?.name || m.productId;
    const from = locations.find(l => l.id === m.from)?.name || m.from || "-";
    const to = locations.find(l => l.id === m.to)?.name || m.to || "-";
    movementTable.innerHTML += `<tr>
      <td>${prod}</td><td>${m.qty}</td>
      <td>${from}</td><td>${to}</td><td>${m.time}</td>
    </tr>`;
  });
}

// Event handlers
productForm.addEventListener("submit", e => {
  e.preventDefault();
  const id = document.getElementById("productId").value;
  const name = document.getElementById("productName").value;
  if (id && name) {
      products.push({id, name});
      localStorage.setItem(PRODUCT_KEY, JSON.stringify(products));
      renderProducts();
      productForm.reset();
  }
});

locationForm.addEventListener("submit", e => {
  e.preventDefault();
  const id = document.getElementById("locationId").value;
  const name = document.getElementById("locationName").value;
  if (id && name) {
      locations.push({id, name});
      localStorage.setItem(LOCATION_KEY, JSON.stringify(locations));
      renderLocations();
      locationForm.reset();
  }
});

movementForm.addEventListener("submit", e => {
  e.preventDefault();
  const productId = movementProduct.value;
  const qty = parseInt(document.getElementById("movementQty").value);
  const from = fromLocation.value;
  const to = toLocation.value;
  const time = new Date().toLocaleString();
  if (productId && qty) {
      movements.push({productId, qty, from, to, time});
      localStorage.setItem(MOVEMENT_KEY, JSON.stringify(movements));
      renderMovements();
      movementForm.reset();
  }
});

// Report generator
function generateReport() {
  let report = {};
  movements.forEach(m => {
    if (m.from) {
      report[m.productId + "_" + m.from] = (report[m.productId + "_" + m.from] || 0) - m.qty;
    }
    if (m.to) {
      report[m.productId + "_" + m.to] = (report[m.productId + "_" + m.to] || 0) + m.qty;
    }
  });

  reportTable.innerHTML = "";
  for (let key in report) {
    const [prodId, locId] = key.split("_");
    const prod = products.find(p => p.id === prodId)?.name || prodId;
    const loc = locations.find(l => l.id === locId)?.name || locId;
    if (report[key] !== 0) {
        reportTable.innerHTML += `<tr><td>${prod}</td><td>${loc}</td><td>${report[key]}</td></tr>`;
    }
  }
}

generateReportBtn.addEventListener('click', generateReport);

// Initial render
renderProducts();
renderLocations();
renderMovements();
generateReport();
