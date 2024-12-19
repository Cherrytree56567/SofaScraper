fetch('SofaData.json')
.then(response => {
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
})
.then(data => {
  console.log(data); // Process the JSON data here
  const JsonData = data;
  var SofaContainer = document.getElementsByClassName("sofa-items")[0];
  var Retailers = JsonData.Retailers;
  console.log(Object.keys(Retailers).length)
  var p = 0;
  for (let Retail in Retailers) {
    var Retailer = Retail;
    var RetailerURL = Retailers[Retail].RetailerURL;
    var Items = Retailers[Retail].Items;
    
    for (let itemKey in Items) {
        const Item = Items[itemKey];
        var SofaName = itemKey;
        var SofaCurrency = Item.Currency;
        var SofaPrice = Item.Price;
        var SofaAttributes = Item.Attributes;
        var SofaVariant = Item.Variant;
        var SofaURL = Item.URL;
        var SofaImages = Item.ImageUrls;
        var codeword = "none";
        if (Retailer == "The Furniture People") {
            codeword = "furnppl";
        }
        if (Retailer == "Amart Furniture") {
            codeword = "amart";
        }
        if (Retailer == "Harvey Norman") {
            codeword = "harvey";
        }
        if (Retailer == "IKEA") {
            codeword = "ikea";
        }
        var SofaCode = `
        <div class="sofa-element ` + codeword + `">
            <div class="sofa-element-image" data-container="slideshow` + p.toString() + `">`
            for (let y = 0; y < SofaImages.length; y++) {
                SofaCode += `<div class="mySlides fade">
                                <a class="prev" onclick="plusSlides(-1, 'slideshow` + p.toString() + `')">&#10094;</a>
                                <a class="next" onclick="plusSlides(1, 'slideshow` + p.toString() + `')">&#10095;</a>
                                <img src="` + SofaImages[y] + `">
                            </div>`;
            }
        
        SofaCode += `</div>
                    <div class="sofa-element-body" onclick="redirect('` + SofaURL + `')">
                        <div class="sofa-element-name">
                            <h2>` + SofaName + ` - ` + SofaVariant + `</h2>
                            <a href="` + RetailerURL + `">` + Retailer + `</a>
                        </div>
                        <br>
                        <div class="sofa-element-price">
                            <b><span>` + SofaCurrency + ` ` + SofaPrice + `</span></b>
                        </div>
                        <span class="attrs">` + SofaAttributes + `</span>
                    </div>
                </div>`
        
        SofaContainer.innerHTML += SofaCode;
        p++;
    }
  }
  document.querySelectorAll("[data-container]").forEach(container => {
    const slides = container.getElementsByClassName("mySlides");
    
    if (slides.length) {
      // Set initial index and show the first slide
      container.dataset.slideIndex = 1;
      showSlides(slides, 1); // Show the first slide on load
    }
  });
  filterSelection('all')
})
.catch(error => {
  console.error('Error fetching JSON:', error);
});

function redirect(url) {
    window.location.href = url;
  }
  