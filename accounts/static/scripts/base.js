//Opens the edit prompt

var def_temp = document.getElementById("def_prompt_template")
function openeditprompt(id){
    if (id!=undefined){
        var modal = new bootstrap.Modal(document.getElementById('prompteditmodal'))
        var form = document.getElementById('editpromptform')
        var name = document.getElementById('editbot_name_')
        var title = document.getElementById('edittitle')
        var description = document.getElementById('editdescription')

        //Clears the previous p tag errors.
        const paragraphs = document.querySelectorAll("form#editpromptform p");    
        paragraphs.forEach(paragraph => {
            paragraph.innerHTML = ""; 
        })

    $.ajax({
        type: 'get',
        url: `fetch_data/${id}`,
        
        success: function(response) {
            //Appends the previous prompt data
            name.value = response.bot_name
            title.value = response.title
            description.innerHTML = response.description
            // Sets the action attribute of prompt with id.
            form.setAttribute("action", `prompt/${id}/`)
            modal.show()
        },
        error: function(response) {
            alert('Error occurred while submitting the form');
        }
        });
    }else{
        $.ajax({
            type: 'get',
            url: 'fetch_data/',
            success: function(response){
                $("#defaultpromptmodal").modal('show')
                def_temp.innerHTML = response.template
                }
            })
    }

    
}

// Save the edited prompt format.
$('#editpromptform').on('submit', function (e){ 
    form = document.getElementById("editpromptform")
    e.preventDefault()  
    $.ajax({
        type: 'post',
        url: form.action,
        data: $(this).serialize() ,
        beforeSend: function (xhr){xhr.setRequestHeader('X-CSRFToken', csrftoken);},
        success: function(response) {
            // Errors show in p tags below the field and modal will not close.
            if (response.errors){ 
            for (var key in response.errors) {
                document.getElementById('ed'+key).innerHTML=response.errors[key]
                }
            $('#prompteditmodal').modal('show');
            }else{
            // On Success it will refresh the page and empty the modal contents.
            location.reload()
            $('#editpromptform').empty()
            $('#prompteditmodal').modal('hide');
            }
        },
        error: function(errors) {
            alert('Error occurred while submitting the form');
        }
    })
});


// To switch the prompts for chatting
function switchprompt(template_id){
    if (template_id != undefined){
        template = document.getElementById("template_id")
        url =`switch_prompt/${template_id}`
    }else{url = 'switch_prompt/'} // to set default prompt
        
    s_p = document.getElementById("selected_prompt")
    
    $.ajax({
        type: 'get',
        url: url,
        success: function(response) {
            s_p.innerText = response.bot_name
            $("#selected_prompt").removeClass("d-none") 
        },
        error: function(response) {
            alert('Unable to switch prompts');
        }
    })
}
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

// Adds new prompt for the User.
$('#promptform').on('submit', function (e){
    e.preventDefault()
    $.ajax({
        type: 'post',
        url: "prompt/",
        data: $(this).serialize() ,
        beforeSend: function (xhr){xhr.setRequestHeader('X-CSRFToken', csrftoken);},
        success: function(response) {
            // Errors show in p tags below the field and modal will not close.
            if (response.errors){ 
            for (var key in response.errors) {
                document.getElementById('e'+key).innerHTML=response.errors[key]
                }
            $('#promptmodal').modal('show');
            }else{
                location.reload()
                $('#promptform').empty()
                $('#promptmodal').modal('hide');
            }
        },
        error: function(errors) {
            alert('Error occurred while submitting the form');
        }
    })
});

// Clears the prompt data on closing and resets the promptform action.
$('#promptmodal').on('hidden.bs.modal', function (e){ 
    var name = document.getElementById('bot_name_')
    var title = document.getElementById('title')
    var description = document.getElementById('description')
    var change_title = document.getElementById('exampleModalLabel')
    var form = document.getElementById('promptform')
    name.value = ''
    title.value = ''
    description.innerHTML = ''
    change_title.innerHTML = "Add Prompt"
    form.setAttribute("action", `prompt/`)
});

var body = document.getElementById("delmodelbody")
var foot = document.getElementById("delmodelfooter")

// Open delete modal and show Prompt Title and Bot Name.
function opendelmodal(title, name, id){
    body.innerHTML = ''
    foot.innerHTML = ''
    $("#delmodal").modal('show')
   
    body.innerHTML = `Are you sure you want to delete Promt with Title - <b>"${title}"</b> and name- <b>"${name}"</b> ?`
    
    foot.innerHTML += `<a href='delete/${id}' class="m-btn ">Delete</a>
    <a href="" type="button" class="btn">No</a>`
}

