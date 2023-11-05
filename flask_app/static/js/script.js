function show_comment_form(id){
    document.getElementById(id).style.display = "block";
}
function hide_comment_form(id){
    document.getElementById(id).style.display = "";
}


function hide_edit_btn(e){
    e.style.display = "none"
}
function show_edit_btn(id){
    document.getElementById(id).style.display = ""
}

function hide_comment_body(id){
    document.getElementById(id).style.display = "none"
}
function show_comment_body(id){
    document.getElementById(id).style.display = ""
}


function show_update_form(id){
    document.getElementById(id).style.display = "block";
}


function hide_add_comment(e){
    e.style.display = "none"
}



function toggleCheckbox(id, consoles_selecter_id) {
    var checkbox = document.getElementById(id);
    checkbox.checked = !checkbox.checked; 

    if (checkbox.checked){
        document.getElementById(consoles_selecter_id).style.borderStyle = "solid";
        document.getElementById(consoles_selecter_id).style.borderColor = "#51d6ff";
        document.getElementById(consoles_selecter_id).style.borderRadius = "15px";
    }else{
        document.getElementById(consoles_selecter_id).style.borderStyle = "";
        document.getElementById(consoles_selecter_id).style.borderColor = "";
    }
}
