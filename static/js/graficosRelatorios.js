function months() {
  return [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
  ];
}

function randomRGBA() {
  let r = Math.floor(Math.random() * 256);
  let g = Math.floor(Math.random() * 256);
  let b = Math.floor(Math.random() * 256);
  let a = 0.5;

  let rgbaColor = "rgba(" + r + "," + g + "," + b + "," + a + ")";
  return rgbaColor;
}

const dateRange = document.querySelector("#dateRange");

document.querySelectorAll('input[name="periodo"]').forEach((item) => {
  item.onclick = () => {
    if (item.id === "radioRange") {
      dateRange.style.display = "grid";
      dateRange.querySelectorAll("input").forEach((inputDate) => {
        inputDate.setAttribute("required", "");
      });
    } else {
      dateRange.style.display = "none";
      dateRange.querySelectorAll("input").forEach((inputDate) => {
        inputDate.removeAttribute("required");
      });
    }
  };
});

let meuGrafico = document.getElementById("meuGrafico");
const myChart = new Chart(meuGrafico.getContext("2d"), {
  type: "bar",
});
const graphicTitle = document.getElementById("graphic_title");

const myForm = document.getElementById("generateReport");

myForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(myForm);
  const params = new URLSearchParams(formData);

  fetch("/reportsJson/?" + params)
    .then((res) => res.json())
    .then((data) => {
      is_month = data.is_month ? true : false;

      updateChart(data.result, is_month);
      graphicTitle.textContent = data.title;
      meuGrafico.style.display = "flex";
    });
});

function updateChart(novosDados, is_month) {
  let dados = {
    labels: is_month ? months() : novosDados.map((i) => i[0]),
    datasets: [
      {
        label: "Valor Total",
        data: novosDados.map((i) => i[1]),
        backgroundColor: novosDados.map(() => randomRGBA()),
        borderWidth: 1,
      },
    ],
  };

  ChartColors.change();

  myChart.data = dados;
  myChart.update();
}

const mesesAnosDiv = document.querySelector(".mesesAnosHide");

document
  .querySelector('select[name="tipoRelatorio"]')
  .addEventListener("input", (event) => {
    is_mes_ano = ["meses", "anos"].includes(event.target.value);

    if (is_mes_ano) {
      mesesAnosDiv.style.display = "none";
      document.querySelector("#todo").checked = true;
      dateRange.querySelectorAll("input").forEach((inputDate) => {
        inputDate.removeAttribute("required");
        inputDate.value = "";
      });
      dateRange.style.display = "none";
    } else {
      mesesAnosDiv.style.display = "block";
    }
  });

class ChartColors {
  static change() {
    let contrastColor = getComputedStyle(
      document.documentElement
    ).getPropertyValue("--contrast");

    let options = {
      scales: {
        y: {
          grid: {
            color: "rgba(0, 0, 0, 0.5)",
          },
          ticks: {
            color: contrastColor,
          },
        },
        x: {
          ticks: {
            color: contrastColor,
          },
        },
      },
    };

    myChart.options = options;
    myChart.update();
  }
}

themeObservable.subscribe(ChartColors);
