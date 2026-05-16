/* script.js */

document.addEventListener("DOMContentLoaded", () => {
    // Loader
    const loader = document.getElementById("loader");
    if (loader) {
        setTimeout(() => {
            loader.style.opacity = "0";
            setTimeout(() => loader.style.display = "none", 500);
        }, 800);
    }

    // Dark Mode Toggle
    const darkModeBtn = document.getElementById("darkModeToggle");
    const body = document.body;
    
    // Check local storage for theme
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        if(darkModeBtn) darkModeBtn.innerHTML = '<i class="bi bi-sun-fill"></i>';
    }

    if (darkModeBtn) {
        darkModeBtn.addEventListener("click", (e) => {
            e.preventDefault();
            body.classList.toggle("dark-mode");
            if (body.classList.contains("dark-mode")) {
                localStorage.setItem("theme", "dark");
                darkModeBtn.innerHTML = '<i class="bi bi-sun-fill"></i>';
            } else {
                localStorage.setItem("theme", "light");
                darkModeBtn.innerHTML = '<i class="bi bi-moon-fill"></i>';
            }
        });
    }

    // Slider Logic (Home Page)
    const track = document.getElementById("sliderTrack");
    const nextBtn = document.getElementById("sliderNext");
    const prevBtn = document.getElementById("sliderPrev");
    
    if (track && nextBtn && prevBtn) {
        const slides = document.querySelectorAll(".slide");
        let currentIndex = 0;
        
        nextBtn.addEventListener("click", () => {
            if (currentIndex < slides.length - 1) {
                currentIndex++;
            } else {
                currentIndex = 0; // loop back
            }
            updateSlider();
        });

        prevBtn.addEventListener("click", () => {
            if (currentIndex > 0) {
                currentIndex--;
            } else {
                currentIndex = slides.length - 1; // loop to end
            }
            updateSlider();
        });

        function updateSlider() {
            track.style.transform = `translateX(-${currentIndex * 100}%)`;
        }
    }

    // Search and Filter Logic (Home Page)
    const searchInput = document.getElementById("searchInput");
    const categoryCards = document.querySelectorAll(".category-item");

    if (searchInput) {
        searchInput.addEventListener("keyup", () => {
            const val = searchInput.value.toLowerCase();
            categoryCards.forEach(card => {
                const title = card.getAttribute("data-title").toLowerCase();
                if (title.includes(val)) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    }

    // Scroll to Top
    const scrollTopBtn = document.getElementById("scrollTopBtn");
    if (scrollTopBtn) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 300) {
                scrollTopBtn.style.display = "block";
            } else {
                scrollTopBtn.style.display = "none";
            }
        });

        scrollTopBtn.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // Product Search Logic (Category Pages)
    const productSearchInput = document.getElementById("productSearchInput");
    const productCols = document.querySelectorAll(".menu-card");

    if (productSearchInput) {
        productSearchInput.addEventListener("keyup", () => {
            const val = productSearchInput.value.toLowerCase();
            productCols.forEach(card => {
                const textContainer = card.querySelector(".p-3");
                const textContent = textContainer ? textContainer.innerText.toLowerCase() : "";

                if (textContent.includes(val)) {
                    card.parentElement.style.display = "";
                } else {
                    card.parentElement.style.display = "none";
                }
            });
        });
    }
});

// Helper for WhatsApp Ordering (Product Pages)
function orderOnWhatsApp(productName) {
    const phoneNumber = "919715948824";
    const message = `Hello Kovai Restaurant, I want to order ${productName}.`;
    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
    window.open(whatsappUrl, "_blank");
}
