
document.addEventListener("DOMContentLoaded", function() {

      var hearts = document.getElementsByClassName("heartLinks");

      [].forEach.call(hearts, heart => {
          heart.addEventListener("click", () => {
              currentPostId = heart.getAttribute("data-id");
              fetch("/hearted", {
                method: 'POST',
                body: JSON.stringify({
                    currentPostId: currentPostId
                })
              })
              .then(response => response.json())
              .then(result => {
                  // Print result
                  console.log(result);
                  var chosenSpan = document.querySelector(`[data-ids='${currentPostId}']`);
                  chosenSpan.innerText = result.postLikes;

              });
          });

      });
})
