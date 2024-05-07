
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












