// 검색 조건을 JSON으로 변환합니다.
function getQuery() {
    return {
      title: document.querySelector("#title").value,
      author: document.querySelector("#author").value,
      category: document.querySelector("#category").value,
      written: {
        min: document.querySelector("#written").value,
        max: document.querySelector("#written2").value,
      },
      pages: {
        min: document.querySelector("#pages").value,
        max: document.querySelector("#pages2").value,
      },
      sell: {
        min: document.querySelector("#sell").value,
        max: document.querySelector("#sell2").value,
      },
    };
  }
  
  // 검색 질의를 수행합니다.
  function search() {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/search");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(getQuery()));
  
    // 검색 결과를 처리합니다.
    xhr.onload = function() {
      if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        const results = response.hits.hits;
  
        // 검색 결과를 표시합니다.
        for (const result of results) {
          const book = result._source;
          console.log(book);
        }
      } else {
        console.log("에러 발생: " + xhr.status);
      }
    };
  }
  
  // 검색 버튼을 누르면 이벤트 핸들러를 실행합니다.
  document.querySelector("button").addEventListener("click", search);
  