function changepassword() {
  const button = document.getElementById("password-button");
  if (button.innerText === "Change Password") {
    button.innerHTML = "Save";
    button.className = "btn btn-success";
    const input = document.createElement("input");
    input.setAttribute("type", "password");
    input.setAttribute("name", "password");
    input.setAttribute("placeholder", "Type new password");
    input.setAttribute("id", "change-password");
    input.setAttribute("class", "form-control");
    const text = document.getElementById("change-password");
    text.replaceWith(input);
  } else {
    const text = document.createElement("li");
    text.setAttribute("id", "change-password");
    text.setAttribute("class", "list-group-item");
    text.innerHTML = "PASSWORD";
    const input = document.getElementById("change-password");
    input.replaceWith(text);
    button.innerHTML = "Change Password";
    button.className = "btn btn-dark";
    const xhr = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/editprofile";
    xhr.open("POST", url, true);
    // xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(
      JSON.stringify({
        value: input.value,
        type: "password",
      })
    );
  }
}
function changeemail() {
  const button = document.getElementById("email-button");
  if (button.innerText === "Change Email") {
    button.innerHTML = "Save";
    button.className = "btn btn-success";
    const input = document.createElement("input");
    input.setAttribute("type", "email");
    input.setAttribute("name", "email");
    input.setAttribute("placeholder", "Type new email");
    input.setAttribute("id", "change-email");
    input.setAttribute("class", "form-control");
    const text = document.getElementById("email");
    text.replaceWith(input);
  } else {
    const input = document.getElementById("change-email");
    const xhr = new XMLHttpRequest();
    const url = "http://127.0.0.1:5000/editprofile";
    xhr.open("POST", url, true);
    // xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(
      JSON.stringify({
        value: input.value,
        type: "email",
      })
    );
    location.reload();
  }
}
