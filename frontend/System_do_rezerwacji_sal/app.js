const hamburger = document.querySelector('.header .nawigacja .lista-nawigacji .hamburger');
const mobile_menu = document.querySelector('.header .nawigacja .lista-nawigacji ul');

hamburger.addEventListener('click',()=> {
    hamburger.classList.toggle('active');
    mobile_menu.classList.toggle('active');
});

