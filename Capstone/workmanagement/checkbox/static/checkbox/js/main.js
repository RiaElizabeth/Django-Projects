document.addEventListener('DOMContentLoaded', function() {
    document.querySelector("#view").addEventListener('click', view_team)
  });

function view_team() {
    document.querySelector("#content").style.display = 'none';
    document.querySelector("#data").style.display = 'block';
    var current_user;
    fetch(`/current_user`)
    .then(response => response.json())
    .then(user => {
      current_user = user.current_user;
      console.log(current_user);
    fetch(`/display_teams`)
    .then(response => response.json())
    .then(teams => {
        // console.log(teams);
        teams.forEach(element => {
          //console.log(element);
          var userbd = document.createElement('ul');
          for (let index = 0; index < element.user.length; index++) {
            let li = document.createElement('li');
            li.innerHTML = element.user[index];
            userbd.appendChild(li)
          }
          if(current_user==element.owner) {
            userbd.innerHTML+="<br/>";
            let an = document.createElement('a');
            an.innerText = 'Manage'; 
            an.href = "/editteam/"+ element.id;
            userbd.appendChild(an);
          }
          console.log(userbd);
          const trow = document.createElement('tr');
          trow.innerHTML = `<th scope="row">${element.title}</th>`;
          trow.innerHTML+=`<td>${element.owner} <i>(Owner)</i> <br><br><b>Members: </b>`+userbd.innerHTML+`</td>`;
          document.getElementById("table-body").appendChild(trow);
        });
    }).catch(err => {
      console.log("Error: "+err);
    });
  });
}
  