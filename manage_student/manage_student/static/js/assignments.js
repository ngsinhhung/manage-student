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

function check_semeter(id, type) {
    var total_seme = document.getElementById(`total-seme-${id}`)
    var seme1 = document.getElementById(`seme1-${id}`)
    var seme2 = document.getElementById(`seme2-${id}`)
    total_seme.value = "False"
    seme1.value = "False"
    seme2.value = "False"

    if (type === 'total') {
        if (!total_seme.checked) {
            seme1.checked = false
            seme2.checked = false
        } else if (total_seme.checked) {
            total_seme.value = "True"
            seme1.checked = true
            seme2.checked = true
            seme1.value = "True"
            seme2.value = "True"
        }
    } else if (type === 'part') {
        if (seme1.checked && seme2.checked) {
            total_seme.checked = true
            total_seme.value = "True"
            seme1.value = "True"
            seme2.value = "True"
        } else if (seme1.checked) {
            total_seme.checked = false
            seme1.value = "True"
        } else if (seme2.checked) {
            total_seme.checked = false
            seme2.value = "True"
        } else {
            total_seme.checked = false
        }
    }
}

