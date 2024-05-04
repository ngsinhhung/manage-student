function setupInputValidation() {
    document.querySelectorAll('.score_15p, .score_45p, .score_final').forEach(function (input) {
        input.addEventListener('input', function () {
            validateInput(input);
        });
    });
}

function validateInput(input) {
    var value = parseFloat(input.value);
    var errorMessage = document.getElementById("message-error");
    var parentAlter = document.getElementById("alterMessage");

    var isValid = true;
    var message = "";

    if (value >= 0 && value <= 10) {
        message = "Điểm phải là số từ 0 đến 10";
        isValid = false;
    } else if (value < 0) {
        message = "Điểm không được âm";
        isValid = false;
    } else if (value > 10) {
        message = "Điểm không được lớn hơn 10";
        isValid = false;
    }

    errorMessage.innerHTML = message;
    parentAlter.style.display = isValid ? 'none' : 'flex';
    return isValid;
}
document.addEventListener("DOMContentLoaded", function () {
    setupInputValidation();
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

            document.getElementById("exportButton").disabled = false
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
            document.getElementById("exportButton").disabled = false
        })
        .catch(function (error) {
            console.error("Error:", error);
            fail("Error updating scores: " + error.message);
        });
}

function updateUI(data) {
    const successButton = document.getElementById("updateButton")
    Object.keys(data).forEach(function (studentId) {
        var studentData = data[studentId];
        const btnEdit = document.getElementById(`btn-action-edit_${studentId}`)
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
    var score15pInputs = document.querySelectorAll(`input[name^='score_15p_student_${studentId}']`);
    var score45pInputs = document.querySelectorAll(`input[name^='score_45p_student_${studentId}']`);
    var scoreFinalInput = document.getElementById(`score_thi_student_${studentId}`);


    score15pInputs.forEach(function (input) {
        input.disabled = false;
    });

    score45pInputs.forEach(function (input) {
        input.disabled = false;
    });

    scoreFinalInput.disabled = false;

    // Ẩn nút "Chỉnh sửa" và hiển thị nút "Xác nhận chỉnh sửa"
    document.getElementById(`btn-action-edit_${studentId}`).style.display = 'none';
    document.getElementById(`btn-action-approved_${studentId}`).style.display = 'inline-block';
    document.getElementById(`btn-action-cancel_${studentId}`).style.display = 'block'
}

function approvedEditStudent(studentId) {
    var score15pInputs = document.querySelectorAll(`input[name^='score_15p_student_${studentId}']`);
    var score45pInputs = document.querySelectorAll(`input[name^='score_45p_student_${studentId}']`);
    var scoreFinalInput = document.getElementById(`score_thi_student_${studentId}`);

    var score15pValues = [];
    var score45pValues = [];

    score15pInputs.forEach(function (input) {
        score15pValues.push(input.value);
    });

    score45pInputs.forEach(function (input) {
        score45pValues.push(input.value);
    });

    const data = {
        "score_15p": score15pValues,
        "score_45p": score45pValues,
        "score_final": scoreFinalInput.value
    }

    fetch('/api/exam/' + studentId + '/edit_score', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error updating scores');
            }
            return response.json();
        })
        .then(data => {
            success("Sửa điểm thành công")
            document.getElementById(`btn-action-approved_${studentId}`).style.display = 'none';
              document.getElementById(`btn-action-edit_${studentId}`).style.display = 'block';
            console.log('Update successful:', data);
        })
        .catch(error => {
            console.error('Update error:', error);
        });
}

function cancelUpdateScore(studentId) {
    document.getElementById(`btn-action-edit_${studentId}`).style.display = 'block'
    document.getElementById(`btn-action-approved_${studentId}`).style.display = 'none';
    document.getElementById(`btn-action-cancel_${studentId}`).style.display = 'none'
    var score15pInputs = document.querySelectorAll(`input[name^='score_15p_student_${studentId}']`);
    var score45pInputs = document.querySelectorAll(`input[name^='score_45p_student_${studentId}']`);
    var scoreFinalInput = document.getElementById(`score_thi_student_${studentId}`);


    score15pInputs.forEach(function (input) {
        input.disabled = true
    });

    score45pInputs.forEach(function (input) {
        input.disabled = true
    });
    scoreFinalInput.disabled = true

}

function createExcel(data, columns, fileName) {
    const ws = XLSX.utils.aoa_to_sheet([columns, ...data]);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

    const wscols = [
        {wpx: 80},
        {wpx: 200},
        {wpx: 120},
        {wpx: 100},
        {wpx: 100},
        {wpx: 100}
    ];
    ws['!cols'] = wscols;

    XLSX.writeFile(wb, fileName);
}

function getDataFromInputs() {
    const data = [];
    const rows = document.querySelectorAll('table tbody tr');

    rows.forEach(row => {
        const rowData = [];
        const score15pInputs = row.querySelectorAll('.score_15p');
        const score45pInputs = row.querySelectorAll('.score_45p');
        const scoreThiInput = row.querySelector('input[id^="score_thi_student"]');

        const stt = row.querySelector('td:nth-child(1)').innerText;
        rowData.push(stt);

        const studentName = row.querySelector('td:nth-child(2)').innerText;
        rowData.push(studentName);

        const dob = row.querySelector('td:nth-child(3)').innerText;
        rowData.push(dob);

        const score15pValues = Array.from(score15pInputs).map(input => input.value);
        rowData.push(score15pValues.join(' '));

        const score45pValues = Array.from(score45pInputs).map(input => input.value);
        rowData.push(score45pValues.join(' '));

        const scoreThiValue = scoreThiInput.value;
        rowData.push(scoreThiValue);

        data.push(rowData);
    });

    return data;
}


document.getElementById('exportButton').addEventListener('click', function () {
    const data = getDataFromInputs();
    const columns = ['STT', 'Tên Học Sinh', 'Ngày Sinh', 'Điểm 15 phút', 'Điểm 45 phút', 'Điểm Thi'];
    createExcel(data, columns, 'student_scores.xlsx');
});












