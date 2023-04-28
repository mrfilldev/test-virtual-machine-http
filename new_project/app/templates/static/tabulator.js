$(document).ready(function () {
    var url = 'https://cp.simpple.ru/api/v1/widgets/ratings/753bf174295992b3ca2d0bd4a78d6598/popular&limit=8';
    $.get(url, function (response) {
        // Инициализируем таблицу
        return new Tabulator('#example-table', {
            data: JSON.parse(response),
            layout: 'fitColumns',
            columns: [
                {title: 'Статья', field: 'title', width: 550},
                {title: 'Количество голосов', field: 'countRates', align: 'left', formatter: 'progress'},
                {title: 'Средняя оценка', field: 'rating'}
            ]
        })
    });
});