// alert('If you see this alert, then your custom JavaScript script has run!')
let mainSections = document.querySelectorAll("main section");
let lastId;
let cur = [];
var part_1 = document.querySelector("#part_1_title");

let entryPoint = document.querySelectorAll("div#react-entry-point");


window.addEventListener("scroll", event => {
    let mainNavLinks = entryPoint[0].childNodes[0].childNodes[0].childNodes[2].childNodes[0].childNodes[0].childNodes[0].childNodes[0].childNodes;
    let fromTop = window.scrollY;
    // console.log(mainNavLinks);
    mainNavLinks.forEach(link => {
        // let section = document.querySelector(link.hash);
        let section = link;
        // console.log(section);
        // console.log(fromTop);

        if (section.offsetTop <= fromTop && section.offsetTop + section.offsetHeight > fromTop
        ) {
            console.log(link);
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
});