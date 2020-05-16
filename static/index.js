let counter = 1;
const quantity = 20;
const max = 5000;

document.addEventListener("DOMContentLoaded", load);
window.onscroll = () => {
  if (window.scrollY + window.innerHeight >= document.body.offsetHeight) {
    load();
  }
};

function load() {
  const start = counter;
  const end = start + quantity - 1;
  if (counter <= max) {
    counter = end + 1;
    const request = new XMLHttpRequest();
    request.open("post", "/dashboard");
    request.onload = () => {
      const data = JSON.parse(request.response);
      data.forEach(add_post);
    };
    const data = new FormData();
    data.append("start", start);
    data.append("end", end);

    request.send(data);
  }
}

function add_post(contents) {
  const post = `<input type="hidden" name="isbns" value="${contents.isbn}" />
        <tr>
          <td>${contents.isbn}</td>
          <td>${contents.title}</td>
          <td>${contents.author}</td>
          <td>${contents.year}</td>
          <td>
            <button type="submit" class="btn btn-primary mb-2">View</button>
          </td>
        </tr>`;

  //create a hide button
  // const hide = document.createElement("button");
  // hide.className = "hide";
  // hide.innerHTML = "hide";
  // post.append(hide);
  document.querySelector("#books").append(post);
}
document.addEventListener("click", (event) => {
  const element = event.target;
  if (element.className == "hide") {
    element.parentElement.style.animationPlayState = "running";
    element.parentElement.addEventListener("animationend", () => {
      element.parentElement.remove();
    });
  }
});
