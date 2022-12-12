function chstatus(proid){
    let vari=document.getElementById(proid+'status').value
    console.log(vari)
    $.ajax({
        url: "change-status",
        type: "GET",
        data:{id:proid,value:vari},
        success: function (data) {
            console.log(data)
        },
        error: function (err) {
           alert(err);
        },
    });    
}

function block(id){
    Swal.fire({
        title: 'Do you want to block the user?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire(
            'Blocked!',
            'user was Blocked.',
            'success'
          )
          const myTimeout = setTimeout(reponse, 1000);
          function reponse(){
            $.ajax({
                url: "blck!"+id,
                type: "GET",
                data:{idi:id},
                success: function (data) {
                   location.href=data.page;
                },
                error: function (err) {
                   alert(err);
                },
            }); 
          }
        }
     })
    }

function unblock(id){
    Swal.fire({
        title: 'Do you want to Unblock the user?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
      }).then((result) => {
        if (result.isConfirmed) {
          Swal.fire(
            'Unblocked!',
            'user was Unblocked.',
            'success'
          )
          const myTimeout = setTimeout(reponse, 1000);
          function reponse(){
            $.ajax({
                url: "unblck!"+id,
                type: "GET",
                data:{idi:id},
                success: function (data) {
                   location.href=data.page;
                },
                error: function (err) {
                   alert(err);
                },
            }); 
          }
        }
     })
}