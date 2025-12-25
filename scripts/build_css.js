// scripts/build_css.js
const fs = require('fs');
const path = require('path');
const postcss = require('postcss');
const tailwindcss = require('@tailwindcss/postcss');
const autoprefixer = require('autoprefixer');

const INPUT_FILE = path.resolve('./static/src/input.css');
const OUTPUT_FILE = path.resolve('./static/css/styles.css');

// Assurez-vous que le dossier de sortie existe
if (!fs.existsSync(path.dirname(OUTPUT_FILE))) {
    fs.mkdirSync(path.dirname(OUTPUT_FILE), { recursive: true });
}

fs.readFile(INPUT_FILE, (err, css) => {
  if (err) throw err;

  postcss([
    tailwindcss(path.resolve('./tailwind.config.js')), 
    autoprefixer, 
  ])
    .process(css, { from: INPUT_FILE, to: OUTPUT_FILE })
    .then(result => {
      fs.writeFileSync(OUTPUT_FILE, result.css);
      console.log(`✅ CSS compilé et écrit dans : ${OUTPUT_FILE}`);
    })
    .catch(error => {
      console.error('❌ Erreur de compilation PostCSS :', error);
    });
});
