// let productContainer = document.getElementById("products");
// let search = document.getElementById("search");
// let productlist = productContainer.querySelectorAll("div");

// search.addEventListener("keyup", function () {
//   enteredValue = event.target.value.toUpperCase();

//   for (count = 0; count < productlist.length; count = count + 1) {
//     var productname = productlist[count].querySelector("p").textContent;

//     if (productname.toUpperCase().indexOf(enteredValue) < 0) {
//       productlist[count].style.display = "none";
//     } else {
//       productlist[count].style.display = "block";
//     }
//   }
// });

document.getElementById('search').addEventListener('input', function () {
  const searchValue = this.value.toLowerCase(); // Get the input value and convert to lowercase
  const productBoxes = document.querySelectorAll('.product-box'); // Get all product boxes

  productBoxes.forEach(box => {
    const productName = box.getAttribute('data-name'); // Get the product name from data-name
    if (productName.includes(searchValue)) {
      box.style.display = 'block'; // Show the product if it matches
    } else {
      box.style.display = 'none'; // Hide the product if it doesn't match
    }
  });
});
