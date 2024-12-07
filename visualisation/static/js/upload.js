document.addEventListener('DOMContentLoaded', function() {
    const parcourirChart = document.getElementById('parcourir_chart');
    const statisticsOptions = document.getElementById('statistics_options');
    const searchOptions = document.getElementById('search_options');
    const slicingOptions = document.getElementById('slicing_options');
    const parcourirRows = document.getElementById('parcourir_rows');
    const rowInputs = document.getElementById('row_inputs');
    

    function hideAllOptions() {
        statisticsOptions.classList.add('hidden');
        searchOptions.classList.add('hidden');
        slicingOptions.classList.add('hidden');
        if (rowInputs) rowInputs.classList.add('hidden');
    }

    parcourirChart.addEventListener('change', function() {
        hideAllOptions();
        switch(this.value) {
            case 'Statistics':
                statisticsOptions.classList.remove('hidden');
                break;
            case 'FindElem':
                searchOptions.classList.remove('hidden');
                break;
            case 'Slicing':
                slicingOptions.classList.remove('hidden');
                break;
        }
    });

    if (parcourirRows) {
        parcourirRows.addEventListener('change', function() {
            const inputs = rowInputs.querySelectorAll('input');
            inputs.forEach(input => input.classList.add('hidden'));

            switch(this.value) {
                case 'NbrOfRowsTop':
                    document.getElementById('Head').classList.remove('hidden');
                    break;
                case 'NbrOfRowsBottom':
                    document.getElementById('Tail').classList.remove('hidden');
                    break;
                case 'FromRowToRow':
                    document.getElementById('FromRowNumb').classList.remove('hidden');
                    document.getElementById('ToRowNumb').classList.remove('hidden');
                    break;
            }
            rowInputs.classList.remove('hidden');
        });
    }
});
