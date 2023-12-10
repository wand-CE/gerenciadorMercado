let clienteSelect = document.querySelector("#id_cliente");

let formCliente = document.getElementById("addClienteForm");

let closeOpenModalCliente = window.closeOpenModalCliente;
let url_cliente_json = window.url_cliente_json;
let url_search_products = window.url_search_products;

formCliente.addEventListener("submit", function (event) {
  event.preventDefault();

  const formData = new FormData(formCliente);

  fetch(url_cliente_json, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (!data.errors) {
        let opcao = document.createElement("option");
        opcao.value = data.cliente_id;
        opcao.textContent = data.nome;

        clienteSelect.appendChild(opcao);
        clienteSelect.value = opcao.value;

        closeOpenModalCliente();
        formCliente.reset();
        formCliente
          .querySelectorAll(".errorlist")
          .forEach((item) => (item.innerHTML = ""));
      } else {
        formCliente
          .querySelectorAll(".errorlist")
          .forEach((item) => (item.innerHTML = ""));
        for (const field in data.errors) {
          if (data.errors.hasOwnProperty(field)) {
            let element = formCliente.querySelector(`[name=${field}]`);

            const errorMessages = data.errors[field];

            let errorList = formCliente.querySelector(`.errors_${field}`);

            if (!errorList) {
              let error = document.createElement("ul");
              error.className = `errorlist errors_${field}`;
              formCliente.insertBefore(error, element);

              errorList = error;
            } else {
              errorList.innerHTML = "";
            }

            errorMessages.forEach((errorMessage) => {
              let error = document.createElement("li");

              error.textContent = errorMessage;
              errorList.appendChild(error);
            });
          }
        }
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

let search_products_input = document.getElementById("search_products");
let table_body = document.querySelector(".selectedProdutos");
const searchResults = document.getElementById("searchResults");

document.addEventListener("click", (event) => {
  if (!(event.target === search_products_input)) {
    searchResults.style.display = "none";
  }
});

search_products_input.addEventListener("input", () => {
  let valor = search_products_input.value;
  searchResults.innerHTML = "";
  if (valor.trim()) {
    fetch(`${url_search_products}?nameProduct=${valor}`)
      .then((res) => res.json())
      .then((data) => {
        searchResults.style.display = "block";

        let quant_produtos = data.produtos.length;
        if (quant_produtos) {
          data.produtos.forEach((result) => {
            if (!table_body.querySelector(`[data-produto_id="${result.id}"]`)) {
              const resultItem = document.createElement("div");

              resultItem.classList.add("result-item");
              resultItem.textContent = `Produto: ${result.nome} - Qtd. Estoque: ${result.quantidade} - Preço: R$${result.preco}`;
              for (const key in result) {
                if (Object.prototype.hasOwnProperty.call(result, key)) {
                  resultItem.dataset[key] = result[key];
                }
              }
              resultItem.addEventListener("click", () => {
                if (parseInt(result.quantidade)) {
                  addProdutoTable(
                    result.id,
                    result.nome,
                    result.categoria,
                    result.preco,
                    result.quantidade
                  );
                  resultItem.remove();
                  if (!searchResults.children.length) {
                    searchResults.style.display = "none";
                  }
                } else {
                  alert("Produto em falta");
                }
              });

              if (result.id !== data.produtos[quant_produtos - 1].id) {
                resultItem.style.borderBottom =
                  "2px solid var(--contrast-inverse)";
              }
              searchResults.appendChild(resultItem);
            }
          });
          if (!searchResults.children.length) {
            searchResults.style.display = "none";
          }
        } else {
          const resultItem = document.createElement("div");
          resultItem.classList.add("result-item");
          resultItem.textContent = "Nenhum produto com esse nome";
          searchResults.appendChild(resultItem);
        }
      });
  } else {
    let atual = searchResults.style.display;
    searchResults.style.display = atual === "block" ? "none" : "block";

    if (!searchResults.children.length) {
      searchResults.style.display = "none";
    }
  }
});

function addProdutoTable(id, name, category, price, quantity) {
  let tr_element = document.createElement("tr");

  tr_element.dataset.produto_id = id;

  tr_element.innerHTML = `
    <td>${name}</td>
    <td>${category}</td>
    <td>R$${price.replace(".", ",")}</td>
    <td><input type="number" step='1' class='.input_quantity' data-price='${price}' min='1' value='1' max=${quantity} style="width: 120px;"></td>
    <td class='totalPrice' data-price='${price}'>R$${price
    .toString()
    .replaceAll(".", ",")}</td>
    <td><i class="bi bi-trash"></i></td>`;

  tr_element.querySelector(".bi-trash").addEventListener("click", (event) => {
    event.target.closest("tr").remove();
    updateEntirePurchasePrice();
  });

  changeTotalProductValue(
    tr_element.querySelector("input"),
    tr_element.querySelector(".totalPrice")
  );

  table_body.appendChild(tr_element);

  updateEntirePurchasePrice();
}

function changeTotalProductValue(input, elementToChange) {
  input.addEventListener("input", () => {
    let dotsList = [",", ".", "-"];

    dotsList.forEach((item) => {
      input.value = input.value.replaceAll(item, "");
    });

    let quantity = parseInt(input.value);

    let price = parseFloat(input.dataset.price);

    let totalPrice = quantity * price;
    let totalPriceElement = elementToChange;

    if (!Number.isNaN(totalPrice)) {
      totalPrice = totalPrice.toFixed(2);
      totalPriceElement.dataset.price = totalPrice;
      elementToChange.textContent = `R$${totalPrice
        .toString()
        .replaceAll(".", ",")}`;
    } else {
      totalPriceElement.dataset.price = "0.00";
      elementToChange.textContent = "R$0,00";
    }

    updateEntirePurchasePrice();
  });
}

function updateEntirePurchasePrice() {
  let precoTotal = 0.0;

  table_body
    .querySelectorAll(".totalPrice")
    .forEach((item) => (precoTotal += parseFloat(item.dataset.price)));

  table_body.parentElement.querySelector(
    "#entirePurchasePrice"
  ).textContent = `R$${precoTotal.toFixed(2).toString().replaceAll(".", ",")}`;
}

let form_compra = document.getElementById("form_Compra");

form_compra.addEventListener("submit", (event) => {
  event.preventDefault();

  let produtosLista = [];

  let produtos = [
    ...form_compra.querySelector(".selectedProdutos").querySelectorAll("tr"),
  ];

  if (!produtos.length) {
    alert("Adicione produtos!!!");
    return false;
  }

  let isValid = true;

  produtos.every((item) => {
    let inputNumber = item.querySelector("input[type='number']");
    let inputValue = parseInt(inputNumber.value);

    if (Number.isNaN(inputValue)) {
      isValid = !isValid;

      inputNumber.setAttribute("aria-invalid", true);
      alert("Valor deve ser um número inteiro positivo");
      inputNumber.focus();
      return false;
    }

    let produtoToAdd = {
      id: item.dataset.produto_id,
      quantidade: inputValue,
    };

    produtosLista.push(JSON.stringify(produtoToAdd));
    inputNumber.setAttribute("aria-invalid", false);
    return true;
  });

  if (isValid) {
    let form = new FormData(form_compra);
    form.append("produtos", produtosLista);

    fetch("/registrarCompra/", {
      method: "POST",
      body: form,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          window.location.replace(`${window.location.origin}/listarCompras/`);
        } else {
          [...notification.children].forEach((item) => {
            if (!item.classList.contains("header")) {
              item.remove();
            }
          });
          let message = document.createElement("div");

          message.style.color = "red";
          message.textContent = data.message;

          notification.appendChild(message);
          notification.style.display = "block";

          showNotification(notification);
        }
      });
  }
});

const notification = document.getElementById("notifications");

function showNotification(notification) {
  setTimeout(() => {
    notification.style.display = "none";
  }, 5000);
}
if (notification) {
  showNotification(notification);
}
