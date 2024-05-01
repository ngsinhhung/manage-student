function success(message) {
    toast({
        title: "Thành công",
        message: message,
        type: 'success',
        duration: 5000,
    });
}

function fail(message) {
    toast({
        title: "Thất bại",
        message: message,
        type: 'warning',
        duration: 10000,
    });
}

function updateScores(teachingPlanId) {
    var data = {};

    $("table tbody tr").each(function () {
        var studentId = $(this).find("input[name^='score_15p']").attr('name').split('_')[3];
        var scores_15p = [];
        var scores_45p = [];

        $(this).find("input[name^='score_15p']").each(function () {
            scores_15p.push($(this).val());
        });

        $(this).find("input[name^='score_45p']").each(function () {
            scores_45p.push($(this).val());
        });

        var score_thi = $(this).find("input[name='score_thi_student_" + studentId + "']").val();

        data[studentId] = {
            "score_15p": scores_15p,
            "score_45p": scores_45p,
            "score_final": score_thi
        };
    });

    fetch("/api/exam/" + teachingPlanId + "/scores", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(function (response) {
            if (!response.ok) {
                throw new Error("Error updating scores: " + response.statusText);
            }
            return response.json();
        })
        .then(function (data) {
            updateUI(data);
            success(data.message);
        })
        .catch(function (error) {
            console.error("Error:", error);
            fail("Error updating scores: " + error.message);
        });
}

function updateUI(data) {
    var tbody = document.querySelector("table tbody");
    const successButton = document.getElementById("updateButton")
    Object.keys(data).forEach(function (studentId) {
        var studentData = data[studentId];
        console.log(studentData)
        var row = document.getElementById(`student_${studentId}`);
        if (row) {
            var th = document.createElement("th");
            var td = document.createElement("td");

            // Tạo nút "Sửa điểm" và thêm vào td
            var editButton = document.createElement("button");
            editButton.className = `btn btn-primary ${studentId}`;
            editButton.textContent = "Sửa điểm";
            td.appendChild(editButton);

            // Thêm td vào hàng
            row.appendChild(th);
            row.appendChild(td);
            var inputs_15p = row.querySelectorAll(".score_15p");
            var inputs_45p = row.querySelectorAll(".score_45p");
            var input_thi = row.querySelector(`[name='score_thi_student_${studentId}']`);
            console.log(studentData.score_15p)
            console.log(studentData.score_45p)
            console.log(studentData.score_final)
            if (studentData.score_15p && studentData.score_45p) {
                studentData.score_15p.forEach(function (score, index) {
                    if (inputs_15p[index]) {
                        inputs_15p[index].value = score;
                        inputs_15p[index].disabled = true;
                    }
                });
                studentData.score_45p.forEach(function (score, index) {
                    if (inputs_45p[index]) {
                        inputs_45p[index].value = score;
                        inputs_45p[index].disabled = true;
                    }
                });

                input_thi.value = studentData.score_final
                input_thi.disabled = true

                successButton.disabled = true
                successButton.innerHTML = "Cập nhật điểm thành công"
            } else {
                console.log("Not FOUND")
            }

        } else {
            console.error(`Element with id 'student_${studentId}' not found in DOM.`);
        }
    });
}













