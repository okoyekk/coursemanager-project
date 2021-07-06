document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#register-buttons>#btnradio1').addEventListener('click', () => load_form("user"));
    document.querySelector('#register-buttons>#btnradio2').addEventListener('click', () => load_form("student"));
    document.querySelector('#register-buttons>#btnradio3').addEventListener('click', () => load_form("instructor"));
})


// Make a specific button visible when it is called
function load_form(button) {
    // make div visible and all buttons in div invisible
    let link_div = document.querySelector('.register-links');
    link_div.style.display = 'block';
    let links = link_div.querySelectorAll('form');
    links.forEach(element => {
        element.style.display = 'none';
    });
    // make only parameter form visible
    switch (button) {
        case "user":
            links[0].style.display = 'block';
            break;
        case "student":
            links[1].style.display = 'block';
            break;
        case "instructor":
            links[2].style.display = 'block';
            console.log("ins");
            break;
        default:
            console.log(`Invalid form: ${form}`);
            break;
    }
}
