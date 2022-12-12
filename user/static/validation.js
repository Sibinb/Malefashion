let error1 = true;
let error2 = true;
let error3 = true;
let error4 = true;
const name_error = document.getElementById("name-error");
const usrname_error = document.getElementById("usrname-error");
const email_error = document.getElementById("email-error");
const number_error = document.getElementById("number-error");
const form = document.getElementById("reg-form");

function na(e) {
  const exp = "^[A-Za-z][A-Za-z]{2,10}$";
  val = e.value;
  if (val.length < 3) {
    name_error.innerHTML = "*Name required atleast 3 letters";
    error1 = true;
  } else if (val.match(exp) === null) {
    name_error.innerHTML = "*Letters only";
    error = true;
  } else {
    name_error.innerHTML = "";
    error1 = false;
  }
}

function una(e) {
  val = e.value;
  if (val.length < 3) {
    usrname_error.innerHTML = "*Username required atleast 3 letters";
    error2 = true;
  } else {
    usrname_error.innerHTML = "";
    error2 = false;
  }
}
function em(e) {
  const exp = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$";
  val = e.value;
  if (val.match(exp) === null) {
    email_error.innerHTML = "*Incorrect email";
    error3 = true;
  } else {
    email_error.innerHTML = "";
    error3 = false;
  }
}

function num(e) {
  const exp = "^[0-9]{10,10}$";
  val = e.value;
  if (val.match(exp) === null) {
    number_error.innerHTML = "*Incorrect phoneno";
    error4 = true;
  } else {
    number_error.innerHTML = "";
    error4 = false;
  }
}

document.getElementById("validate").addEventListener("click", (e) => {
  e.preventDefault();
  if (
    error1 != true &&
    error2 != true &&
    error3 != true &&
    error4 != true 
  ) {
    form.submit();
  } else {
    alert("Fill the form");
  }
});
