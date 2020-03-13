"use strict";

$.get('/api/stock_details/<stock_id>', (res) => {
  console.log(res)
  const data = [];
  for (const dailyInfo of res) {
    console.log(res)
    
$('#canvas-container').append (
  `<canvas id="line-chart-${dailyInfo.symbol}" width="100" height="75"></canvas>`
  )
  new Chart(
    $(`#line-chart-${dailyInfo.symbol}`),
    {
      type: 'line',
      data: {
        labels: ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", 
                "13:30", "14:00", "14:30", "15:00", "15:30", "16:00"],
        datasets: [
          {
            label: 'Price Fluctuations',
            data: dailyInfo.data
          }
        ]
      }
    }
  );
}
});
