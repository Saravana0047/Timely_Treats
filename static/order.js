document.addEventListener('DOMContentLoaded', () => {
  const addToCartButton = document.querySelector('.order-button button');
  const sideNavbar = document.querySelector('.navbar');
  const closeNavbarButton = sideNavbar.querySelector('.fa-xmark');

  
  function openNavbar() {
    sideNavbar.style.display = 'block';
  }

  function closeNavbar() {
    sideNavbar.style.display = 'none';
  }

  // Add to cart //

  addToCartButton.addEventListener('click', (event) => {
    event.preventDefault(); 
    openNavbar();
  });

  closeNavbarButton.addEventListener('click', closeNavbar);
});

// Navbar //

sideNavbar = document.querySelector("container");
function shownavbar() {
  sideNavbar.style.right = "0";
}

function closeavbar() {
  sideNavbar.style.right = "-30%";
}


// Function For Payment 
document.querySelectorAll('input[name="payment_method"]').forEach((elem) => {
  elem.addEventListener("change", function(event) {
      var value = event.target.value;
      document.getElementById('upi_section').style.display = value === 'UPI' ? 'block' : 'none';
      document.getElementById('card_section').style.display = value === 'Card' ? 'block' : 'none';
  });
});

// payment Field
document.getElementById('save-continue-button').addEventListener('click', function() {
  document.getElementById('shipping-address').style.display = 'none';
  document.getElementById('payment-field').style.display = 'block';
});

// JavaScript to replace Shipping Address with Payment Section
        document.getElementById("save-continue-button").addEventListener("click", function() {

          document.getElementById("shipping-address").style.display = "none";
          document.getElementById("payment-field").style.display = "block";
      });


// cart icon functinalities 

function toggleCart() {
  const sidebar = document.getElementById('cart-sidebar');
  sidebar.classList.toggle('active');
}
