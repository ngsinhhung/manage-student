document.addEventListener("DOMContentLoaded", function () {
    checkExistingScores();
});

function checkExistingScores() {
    var studentRows = document.querySelectorAll("table tbody tr");
    console.log("studentRows", studentRows);
    studentRows.forEach(function (row) {
        var studentId = row.id.split("_")[1];
        console.log(studentId);
        fetch(`/api/exam/get_score_student/${studentId}/scores`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else if (response.status === 404) {
                    return {}; // Trả về một đối tượng trống nếu không tìm thấy sinh viên
                } else {
                    throw new Error("Error fetching existing scores: " + response.statusText);
                }
            })
            .then(data => {
                if (Object.keys(data).length > 0) {
                    disableInputsAndShowEditButton(row, studentId, data);
                }
            })
            .catch(error => console.error("Error fetching existing scores:", error));
    });
}


function disableInputsAndShowEditButton(row, studentId, data) {
    var score15pInputs = row.querySelectorAll(`input[name^='score_15p_student_${studentId}']`);
    var score45pInputs = row.querySelectorAll(`input[name^='score_45p_student_${studentId}']`);
    var scoresFinalPoints = document.getElementById(`score_thi_student_${studentId}`);
    const successButton = document.getElementById("updateButton")
    const btnEdit = document.getElementById(`btn-action-edit_${studentId}`)
    if (score15pInputs.length > 0 && score45pInputs.length > 0) {
        var isValidData = checkDataValidity(data);
        console.log(data)
        if (isValidData) {
            score15pInputs.forEach(function (input, index) {
                input.value = data.score_15p[index];
                input.disabled = true;

            });

            score45pInputs.forEach(function (input, index) {
                input.value = data.score_45p[index];
                input.disabled = true;
            });
            scoresFinalPoints.value = data.score_final
            scoresFinalPoints.disabled = true

            successButton.innerHTML = "Điểm đã được cập nhật"
            successButton.disabled = true

            btnEdit.innerHTML = "Chỉnh sửa"
            btnEdit.style.display = "block"
        }
    }
}

function checkDataValidity(data) {
    return data.hasOwnProperty("score_15p") && data.score_15p.length > 0 &&
        data.hasOwnProperty("score_45p") && data.score_45p.length > 0 &&
        data.hasOwnProperty("score_final") && data.score_final !== null;
}
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
    const successButton = document.getElementById("updateButton")
    const btnEdit = document.getElementById(`btn-action-edit_${studentId}`)
    Object.keys(data).forEach(function (studentId) {
        var studentData = data[studentId];
        console.log(studentData)
        var row = document.getElementById(`student_${studentId}`);
        if (row) {
            btnEdit.innerHTML = "Chỉnh sửa"
            btnEdit.style.display = "block"
            var inputs_15p = row.querySelectorAll(".score_15p");
            var inputs_45p = row.querySelectorAll(".score_45p");
            var input_thi = row.querySelector(`[name='score_thi_student_${studentId}']`);
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
                successButton.innerHTML = "Điểm đã lưu"


                btnEdit.innerHTML = "Chỉnh sửa"
                btnEdit.style.display = "block"
            } else {
                console.log("Not FOUND")
            }

        } else {
            console.error(`Element with id 'student_${studentId}' not found in DOM.`);
        }
    });
}

function editScore(studentId) {

}












