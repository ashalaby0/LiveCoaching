
let clientCtart = document.getElementById("clientChart").getContext('2d');
let clientChartObject = new Chart(clientCtart, {
      type: 'line',
      data: {
          labels: ["Jan", "Feb", "March", "April", "May", "June"],
          datasets: [{
              label: '# of Clients',
              data: [3, 6, 7, 25, 12, 19],
              backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
              ],
              borderColor: [
                  'rgba(255,99,132,1)',
              ],
              borderWidth: 1
          }]
      },
      options: {
        legend: {
            display:false,
            labels: {
                fontColor: "white",
            }
        },
          scales: {
              yAxes: [{
                  ticks: {
                    fontColor:"black",
                      beginAtZero:true
                  }
              }],
              xAxes: [{
                ticks: {
                    fontColor:"black"
                }
              }]
          }
      }
  });

  let sessionCtart = document.getElementById("sessionChart").getContext('2d');
  let sessionChartObject = new Chart(sessionCtart, {
        type: 'bar',
        data: {
            labels: ["Jan", "Feb", "March", "April", "May", "June"],
            datasets: [{
                label: '# of Sessions',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(54, 162, 235, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            legend: {
            display:false,
            labels: {
                    fontColor: "white",
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                      fontColor:"black",
                        beginAtZero:true
                    }
                }],
                xAxes: [{
                  ticks: {
                      fontColor:"black"
                  }
                }]
            }
      }
    });
  
  