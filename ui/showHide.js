function showButton(element) {
    document.getElementById('typeButton').style.display = element.value == "gpio_13" ? 'block' : 'none';
}
function showButtonPlus(element) {
    document.getElementById('buttonPressKey').style.display = element.value == "key" ? 'block' : 'none';
    document.getElementById('buttonTypeText').style.display = element.value == "text" ? 'block' : 'none';
    document.getElementById('buttonCustomFunction').style.display = element.value == "custom" ? 'block' : 'none';
}
function buttonKeyValidation(element) {
    document.getElementById('buttonKeyValidate').style.display = element.value != "none" ? 'block' : 'none';
}
function buttonTextValidation(element) {
    document.getElementById('buttonTextValidate').style.display = element.value != "" ? 'block' : 'none';
}
function buttonCustomValidation(element) {
    document.getElementById('buttonCustomValidate').style.display = element.value != "" ? 'block' : 'none';
}