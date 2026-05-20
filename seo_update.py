import os
import re
from bs4 import BeautifulSoup

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    
    filename = os.path.basename(filepath)
    is_index = filename == 'index.html'
    
    # 1. Update <head>
    head = soup.find('head')
    if head:
        # Remove existing title
        if head.find('title'):
            title_text = head.find('title').text
            head.find('title').decompose()
        else:
            title_text = f"Kovai Restaurant | {filename.replace('.html', '').replace('-', ' ').title()}"
            
        if is_index:
            new_title = "Kovai Restaurant | Best Restaurant in Coimbatore"
            desc = "Experience the best Biryani and premium dining at Kovai Restaurant in Gandhipuram, Coimbatore. Family restaurant, fresh food, and 24x7 delivery."
        else:
            page_name = filename.replace('.html', '').replace('-', ' ').title()
            new_title = f"Kovai Restaurant | Best {page_name} in Coimbatore"
            desc = f"Order the best {page_name} at Kovai Restaurant in Gandhipuram, Coimbatore. Premium quality food with 24x7 delivery."

        # Prepare new tags
        seo_tags = f"""
    <title>{new_title}</title>
    <meta name="description" content="{desc}">
    <meta name="keywords" content="Best Restaurant in Coimbatore, Best Biryani in Gandhipuram, Family Restaurant in Coimbatore, Food Delivery in Coimbatore, Restaurant Near Me, Kovai Restaurant, {page_name if not is_index else 'Premium Dining'}">
    <meta name="author" content="Kovai Restaurant">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://kovai-restaurant.vercel.app/{filename}">

    <!-- Open Graph Tags -->
    <meta property="og:title" content="{new_title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="https://kovai-restaurant.vercel.app/images/chicken_1778911981600.png">
    <meta property="og:url" content="https://kovai-restaurant.vercel.app/{filename}">
    <meta property="og:type" content="restaurant.restaurant">

    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{new_title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="https://kovai-restaurant.vercel.app/images/chicken_1778911981600.png">

    <!-- Preconnect for Performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <!-- Schema Markup -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Restaurant",
      "name": "Kovai Restaurant",
      "image": "https://kovai-restaurant.vercel.app/images/chicken_1778911981600.png",
      "@id": "https://kovai-restaurant.vercel.app",
      "url": "https://kovai-restaurant.vercel.app",
      "telephone": "+91 8754678824",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Gandhipuram",
        "addressLocality": "Coimbatore",
        "addressRegion": "Tamil Nadu",
        "postalCode": "641012",
        "addressCountry": "IN"
      }},
      "geo": {{
        "@type": "GeoCoordinates",
        "latitude": 11.0183,
        "longitude": 76.9725
      }},
      "openingHoursSpecification": {{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": [
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday",
          "Sunday"
        ],
        "opens": "00:00",
        "closes": "23:59"
      }},
      "servesCuisine": ["Indian", "Biryani", "Fast Food"],
      "priceRange": "$$"
    }}
    </script>
"""
        # Parse the new tags and insert them at the top of head, after charset and viewport if possible
        seo_soup = BeautifulSoup(seo_tags, 'html.parser')
        
        # Avoid inserting duplicates if script is run multiple times
        if not head.find('meta', {'name': 'description'}):
            viewport = head.find('meta', {'name': 'viewport'})
            if viewport:
                viewport.insert_after(seo_soup)
            else:
                head.insert(0, seo_soup)
    
    # 2. Image SEO
    for img in soup.find_all('img'):
        if not img.get('loading'):
            img['loading'] = 'lazy'
        if not img.get('decoding'):
            img['decoding'] = 'async'
            
        alt_text = img.get('alt', '')
        if alt_text and 'Kovai Restaurant' not in alt_text:
            img['alt'] = f"{alt_text} at Kovai Restaurant Coimbatore"
        elif not alt_text:
            img['alt'] = "Delicious food at Kovai Restaurant Coimbatore"

    # 3. Accessibility (Aria labels)
    for btn in soup.find_all('button'):
        if not btn.text.strip() and not btn.get('aria-label'):
            if btn.get('id') == 'sliderPrev': btn['aria-label'] = 'Previous slide'
            elif btn.get('id') == 'sliderNext': btn['aria-label'] = 'Next slide'
            elif btn.get('id') == 'scrollTopBtn': btn['aria-label'] = 'Scroll to top'
            elif 'navbar-toggler' in btn.get('class', []): btn['aria-label'] = 'Toggle navigation'
            
    for a in soup.find_all('a'):
        if not a.text.strip() and not a.get('aria-label'):
            title = a.get('title')
            if title:
                a['aria-label'] = title
            elif a.get('id') == 'darkModeToggle':
                a['aria-label'] = 'Toggle Dark Mode'
                
    # 4. Updates specific to index.html (Reviews and Maps)
    if is_index:
        # Check if reviews already exist
        if not soup.find(id='reviewsSection'):
            reviews_html = """
    <!-- Customer Reviews Section -->
    <section class="container mb-5" id="reviewsSection" data-aos="fade-up">
        <h2 class="text-center mb-4 gradient-text fw-bold">What Our Customers Say</h2>
        <div class="row g-4">
            <div class="col-md-4">
                <div class="card h-100 shadow-sm border-0 p-3" style="background: var(--bg-card); color: var(--text-color);">
                    <div class="card-body text-center">
                        <div class="text-warning mb-2 fs-5">
                            <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
                        </div>
                        <p class="card-text">"Best biryani in Coimbatore! The taste is authentic and the portion sizes are great. Highly recommended."</p>
                        <h6 class="fw-bold mt-3 mb-0">- Rahul Sharma</h6>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100 shadow-sm border-0 p-3" style="background: var(--bg-card); color: var(--text-color);">
                    <div class="card-body text-center">
                        <div class="text-warning mb-2 fs-5">
                            <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
                        </div>
                        <p class="card-text">"Excellent family restaurant. The ambiance is great, and the chicken dishes are crispy and delicious."</p>
                        <h6 class="fw-bold mt-3 mb-0">- Priya Dinesh</h6>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100 shadow-sm border-0 p-3" style="background: var(--bg-card); color: var(--text-color);">
                    <div class="card-body text-center">
                        <div class="text-warning mb-2 fs-5">
                            <i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i><i class="bi bi-star-fill"></i>
                        </div>
                        <p class="card-text">"Affordable and tasty food. Their juices and milkshakes are perfectly made. My go-to place for dinner."</p>
                        <h6 class="fw-bold mt-3 mb-0">- Arvind K.</h6>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""
            reviews_soup = BeautifulSoup(reviews_html, 'html.parser')
            footer = soup.find('footer', id='contactSection')
            if footer:
                footer.insert_before(reviews_soup)
                
        # Insert Google Maps in the footer
        footer = soup.find('footer', id='contactSection')
        if footer and not footer.find('iframe'):
            # The footer has multiple rows. The second row has "Contact Info" and "Quick Links".
            # We can insert a map before the contact info row, or inside it.
            # "Place it properly in contact/footer section WITHOUT changing existing design."
            # Let's add a row above the contact info inside the footer container.
            
            map_html = """
            <div class="row text-start mt-4 mb-4" data-aos="fade-up">
                <div class="col-12">
                    <h4 class="gradient-text fw-bold mb-3">Find Us Here</h4>
                    <div class="ratio ratio-21x9 shadow-sm" style="border-radius: 10px; overflow: hidden;">
                        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3916.3268800936353!2d76.96349787480854!3d11.014073389149028!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba8585483984bb3%3A0x6b772596be7f6789!2sGandhipuram%2C%20Coimbatore%2C%20Tamil%20Nadu!5e0!3m2!1sen!2sin!4v1700000000000!5m2!1sen!2sin" width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                </div>
            </div>
"""
            # find hr
            hr_tags = footer.find_all('hr')
            if len(hr_tags) >= 1:
                map_soup = BeautifulSoup(map_html, 'html.parser')
                hr_tags[0].insert_after(map_soup)

    # Write back to file, using original formatter roughly
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

html_files = [
    'about.html', 'burger.html', 'chicken.html', 'curry.html', 
    'grilled-chicken.html', 'index.html', 'juice.html', 
    'milkshake.html', 'sandwich.html', 'special-menu.html'
]

dir_path = r'c:\Users\HAI\OneDrive\Documents\Bala Restaurent'
for file in html_files:
    full_path = os.path.join(dir_path, file)
    if os.path.exists(full_path):
        process_file(full_path)
        print(f"Processed {file}")
