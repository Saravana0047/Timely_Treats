// Footer effects //

// Scroll Event Listener
window.addEventListener('scroll', function () {
    const footer = document.querySelector('.animated-footer');
    const triggerHeight = document.body.offsetHeight - window.innerHeight;
  
    if (window.scrollY > triggerHeight - 50) {
      footer.classList.add('footer-visible');
    } else {
      footer.classList.remove('footer-visible');
    }
  });

var sidenav = document.querySelector(".side-navbar");

function showNavbar() {
  sidenav.style.left = "0";
}

function closeNavbar() {
  sidenav.style.left = "-60%";
}

// cart icon functinalities 

    function toggleCart() {
        const sidebar = document.getElementById('cart-sidebar');
        sidebar.classList.toggle('active');
    }


  // Cart Remove 

  document.addEventListener("DOMContentLoaded", () => {
    const cartSidebar = document.getElementById("cart-sidebar"); // Your cart sidebar element
    const removeLinks = cartSidebar.querySelectorAll(".remove-btn");
  
    removeLinks.forEach(link => {
      link.addEventListener("click", event => {
        event.preventDefault(); // Prevent default link behavior
  
        const cartId = event.target.getAttribute("data-cart-id");
  
        if (confirm("Are you sure you want to remove this item?")) {
          fetch(`/remove/${cartId}`, {
            method: "GET", // Flask route supports GET for deletion
          })
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                
                const cartItem = event.target.closest(".cart-item");
                if (cartItem) {
                  cartItem.remove();
                }
  
                alert(data.message);
              } else {
                alert("Failed to remove the item.");
              }
            })
            .catch(error => {
              console.error("Error:", error);
              alert("An error occurred. Please try again.");
            });
        }
      });
    });
  });
  

//   Quantity Update // ------------------------------------------>>>>>>>>


document.addEventListener('DOMContentLoaded', () => {
  // Attach click listeners to plus and minus buttons
  document.querySelectorAll('.plus-btn, .minus-btn').forEach(button => {
    button.addEventListener('click', function () {
      const cartId = this.getAttribute('data-cart-id'); // Get the cart ID
      const inputField = document.querySelector(`input[data-cart-id="${cartId}"]`); // Target input field
      let quantity = parseInt(inputField.value);

      // Adjust quantity based on button clicked
      if (this.classList.contains('plus-btn')) {
        quantity++;
      } else if (this.classList.contains('minus-btn') && quantity > 1) {
        quantity--;
      }

      // Update the input field value
      inputField.value = quantity;

      // Send updated quantity to the server
      fetch('/update_cart', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cart_id: cartId, quantity: quantity })
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            console.log(`Cart updated: ${cartId} -> ${quantity}`);
          } else {
            console.error('Failed to update cart:', data.message);
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });
});


// footer
document.addEventListener("DOMContentLoaded", () => {
  // Select the "Our Story" link and footer elements
  const ourStoryLink = document.querySelector(".our-story-link");
  const footerContainer = document.querySelector(".footer-container");
  const footerBottom = document.querySelector(".footer-bottom");
  const aboutUsContent = document.querySelector(".about-us");
  const backButton = document.querySelector(".back-to-footer");

  // Add event listener to the "Our Story" link
  ourStoryLink.addEventListener("click", (event) => {
    event.preventDefault(); // Prevent default anchor behavior

    // Hide the original footer content
    footerContainer.style.display = "none";
    footerBottom.style.display = "none";

    // Show the "About Us" content
    aboutUsContent.style.display = "block";
  });

  backButton.addEventListener("click", () => {
    // Show the original footer content
    footerContainer.style.display = "flex"; // Reset to flex for proper layout
    footerBottom.style.display = "block";

    // Hide the "About Us" content
    aboutUsContent.style.display = "none";
  });
});

