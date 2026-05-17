const fs = require('fs');
const path = require('path');

const dir = 'c:/Users/HAI/OneDrive/Documents/Bala Restaurent';
const htmlFiles = [
    'burger.html', 'chicken.html', 'curry.html', 'grilled-chicken.html',
    'juice.html', 'milkshake.html', 'sandwich.html', 'special-menu.html', 'index.html'
];

htmlFiles.forEach(file => {
    const filePath = path.join(dir, file);
    if (!fs.existsSync(filePath)) return;

    let content = fs.readFileSync(filePath, 'utf8');
    const imgRegex = /<img[^>]*src=["']([^"']+)["'][^>]*>/g;

    let match;
    let modified = false;

    // Use replace to easily update content
    const newContent = content.replace(imgRegex, (match, src) => {
        const fullImagePath = path.join(dir, src);
        
        // If image doesn't exist, we replace src with default image
        if (!fs.existsSync(fullImagePath)) {
            // Extract category from src, e.g., 'images/burger/...' -> 'burger'
            const parts = src.split('/');
            if (parts.length >= 3 && parts[0] === 'images') {
                const category = parts[1];
                const fallbackSrc = `images/${category}/default-${category}.jpg`;
                console.log(`Updating ${file}: ${src} -> ${fallbackSrc}`);
                modified = true;
                return match.replace(src, fallbackSrc);
            }
        }
        return match;
    });

    if (modified) {
        fs.writeFileSync(filePath, newContent, 'utf8');
        console.log(`Saved ${file}`);
    }
});
