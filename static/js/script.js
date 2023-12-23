
/*navbar*/

var roundedLogin = document.querySelector(".rounded-login");

var roundedSigin = document.querySelector(".rounded-sigin");

if (roundedLogin.classList.contains("rounded-login") && roundedLogin.classList.contains("active")) {
    roundedLogin.style.border = "2px #FE451E solid";
    roundedLogin.style.textDecoration = "none";

}
else {
    //roundedLogin.style.border = "2px white solid";
    
}

if (roundedSigin.classList.contains("rounded-sigin") && roundedSigin.classList.contains("active")) {
    roundedSigin.style.border = "2px #FE451E solid";
    roundedSigin.style.background = "none";
    roundedSigin.style.textDecoration = "none";
    
} 
else {
    
    //roundedSigin.style.backgroundColor = "#FE451E";
}


/*end navbar*/

/*login*/
//show-hide password login
function password_show_hide() {
    var x = document.getElementById("password");
    var show_eye = document.getElementById("show_eye");
    var hide_eye = document.getElementById("hide_eye");
    hide_eye.classList.remove("d-none");
    if (x.type === "password") {
      x.type = "text";
      show_eye.style.display = "none";
      hide_eye.style.display = "block";
    } else {
      x.type = "password";
      show_eye.style.display = "block";
      hide_eye.style.display = "none";
    }
  }


/*end login*/


/*back top top*/
let mybutton = document.getElementById("myBtn");

/*montrer le bouton lorsque l'utilisateur scroll vers le bas de 20px par rapport au document */
window.onscroll = function(){scrollFuntion()}

function scrollFuntion()
{
    if(document.body.scrollTop > 20 || document.documentElement.scrollTop > 20)
    {
        mybutton.style.display = "block";

    }
    else
    {
        mybutton.style.display = "none";

    }
}

/*lorsque l'utilisateur click sur le boutton on le renvoie en haut top = 0*/
function topFunction()
{
    document.body.scrollTop = 0; //pour Safari

    document.documentElement.scrollTop = 0; // pour chrome, firefox , IE and Opera
}



/*end back top top*/



/*about*/
let img = $('.img');
$(document).ready(function(){
    // Sélectionner l'image
    

    // Cacher l'image avec slideUp, puis afficher avec slideDown
    img.hide().slideDown(2000);
    
    
});
/* end about*/




/*caroussel register*/
let currentSlide = 0;
const slides = document.querySelectorAll('.form-slide');

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.display = i === index ? 'block' : 'none';
    });
    currentSlide = index;
}

function nextSlide() {
    if (currentSlide < slides.length - 1) {
        showSlide(currentSlide + 1);
    }
}

function prevSlide() {
    if (currentSlide > 0) {
        showSlide(currentSlide - 1);
    }
}


// Afficher la première diapositive au chargement
showSlide(currentSlide);



/* end caroussel register */

