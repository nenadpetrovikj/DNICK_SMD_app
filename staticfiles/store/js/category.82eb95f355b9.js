document.addEventListener('DOMContentLoaded', function() {
  var checkboxes = document.querySelectorAll('.form-check-input');
  var priceRange = document.getElementById('priceRange');
  var rangeValues = document.getElementById('rangeValues');
  var productCards = document.querySelectorAll('.product-card');

  var brandCheckboxes = document.querySelectorAll('.brand-inputs');
  var screenCheckboxes = document.querySelectorAll('.screen-inputs');
  var batteryCheckboxes = document.querySelectorAll('.battery-inputs');
  var processorCheckboxes = document.querySelectorAll('.processor-inputs');
  var osCheckboxes = document.querySelectorAll('.os-inputs');
  
  
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateProducts);
  });

  let priceTimeout;

  priceRange.addEventListener('input', function() {
    rangeValues.innerHTML = this.value;
  
    clearTimeout(priceTimeout);
    priceTimeout = setTimeout(updateProducts, 300);
  });

  priceRange.addEventListener('change', () => {
    clearTimeout(priceTimeout);
    updateProducts();
  });

  function updateProducts() {

    var selectedBrands = Array.from(brandCheckboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.id);

    var selectedScreens = Array.from(screenCheckboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.id);

    var selectedBatteries = Array.from(batteryCheckboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.id);

    var selectedProcessors = Array.from(processorCheckboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.id);

    var selectedOs = Array.from(osCheckboxes)
    .filter(checkbox => checkbox.checked)
    .map(checkbox => checkbox.id);

    var selectedPrice = parseFloat(priceRange.value)

    productCards.forEach(product => {

      var productManufacturer = product.getAttribute('data-specs').split(',')[0];
      var productScreen = product.getAttribute('data-specs').split(',')[1];
      var productBattery = product.getAttribute('data-specs').split(',')[2];
      var productProcessor = product.getAttribute('data-specs').split(',')[3];
      var productOs = product.getAttribute('data-specs').split(',')[4];

      var productPrice = product.getAttribute('data-price');

      var specsMatch = (selectedBrands.length === 0 || selectedBrands.some(brand => brand === productManufacturer)) && (selectedScreens.length === 0 || selectedScreens.some(screen => screen === productScreen)) && (selectedBatteries.length === 0 || selectedBatteries.some(battery => battery === productBattery)) && (selectedProcessors.length === 0 || selectedProcessors.some(cpu => cpu === productProcessor)) && (selectedOs.length === 0 || selectedOs.some(os => os === productOs));

      var priceMatch = isNaN(selectedPrice) || productPrice <= selectedPrice;

      product.style.display = specsMatch && priceMatch ? 'block' : 'none';
    });
  }
});