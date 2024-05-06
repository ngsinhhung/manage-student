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
