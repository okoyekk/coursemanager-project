document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#register-buttons>#btnradio1').addEventListener('click', () => load_form("user"));
    document.querySelector('#register-buttons>#btnradio2').addEventListener('click', () => load_form("student"));
    document.querySelector('#register-buttons>#btnradio3').addEventListener('click', () => load_form("instructor"));
})


// Make a specific form visible when it is called
function load_form(form) {
    // make div visible and all forms in div invisible
    let form_div = document.querySelector('.register-forms');
    form_div.style.display = 'block';
    let forms = form_div.querySelectorAll('form');
    forms.forEach(element => {
        element.style.display = 'none';
    });
    // make only parameter form visible
    switch (form) {
        case "user":
            forms[0].style.display = 'block';
            break;
        case "student":
            forms[1].style.display = 'block';
            break;
        case "instructor":
            forms[2].style.display = 'block';
            console.log("ins");
            break;
        default:
            console.log(`Invalid form: ${form}`);
            break;
    }
}
