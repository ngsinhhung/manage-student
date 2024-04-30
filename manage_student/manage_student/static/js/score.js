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
            "15p": scores_15p,
            "45p": scores_45p,
            "thi": score_thi
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
            alert(data.message); // Assuming your API returns a message field upon success
        })
        .catch(function (error) {
            console.error("Error:", error);
            alert("Error updating scores: " + error.message);
        });
}









