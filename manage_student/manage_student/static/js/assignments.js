function get_class_by_grade() {
    var grade_value = `K${document.getElementById("grade").value}`;
    var class_list = document.getElementById("class-list");
    class_list.innerHTML = ""
    fetch(`/api/class/?q=${grade_value}`, {
        method: 'get',
    }).then(res => res.json()).then(data => {
        data.class_list.forEach(function (c) {
            var option_tag = document.createElement("option");
            option_tag.value = `${c.grade}A${c.count}`
            option_tag.textContent = `${c.grade}A${c.count}`
            class_list.appendChild(option_tag)
        })
    })
}

function check_semeter(id) {
    var total_seme = document.getElementById(`total_year-${id}`)
    var seme1 = document.getElementById(`seme1-${id}`)
    var seme2 = document.getElementById(`seme2-${id}`)

    total_seme.value="False"
    seme1.value="False"
    seme2.value="False"

    if(total_seme.checked){
        total_seme.value = "True"
        seme1.checked = true
        seme2.checked = true
    }
    else if(seme1.checked){
        seme1.value = "True"
        total_seme.checked = false
        seme2.checked = false
    }
    else if(seme2.checked){
        seme2.value = "True"
        total_seme.checked = false
        seme1.checked = false
    }
}
