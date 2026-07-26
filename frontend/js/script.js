// ======================================================
// Upload PDF
// ======================================================

async function uploadPDF(){


    let fileInput = document.getElementById(
        "pdfFile"
    );


    let status = document.getElementById(
        "uploadStatus"
    );


    if(!fileInput.files.length){

        status.innerHTML =
        "❌ Please select a PDF, DOCX or TXT file";
        return;

    }


    let file = fileInput.files[0];


    let formData = new FormData();

    formData.append(
        "file",
        file
    );


    status.innerHTML =
    "⏳ Uploading and indexing document...";


    try{


        let response = await fetch(
            "/upload",
            {
                method:"POST",
                body:formData
            }
        );

        let data;

        try{
            data = await response.json();
        }
        catch(e){
            addMessage(
                "❌ Invalid server response",
                "bot"
            );
            return;
        }


        if(data.success){


            status.innerHTML =
            "✅ Document indexed successfully";


            addMessage(
                "📚 Document uploaded successfully. Ask your questions!",
                "bot"
            );


        }

        else{


            status.innerHTML =
            "❌ "+data.message;

        }



    }

    catch(error){


        console.log(error);


        status.innerHTML =
        "❌ Upload failed";

    }

}





// ======================================================
// Ask Question
// ======================================================


async function askQuestion(){


    let input =
    document.getElementById(
        "question"
    );


    let question =
    input.value.trim();



    if(!question)
        return;



    addMessage(
        question,
        "user"
    );


    input.value="";



    try{


        let response =
        await fetch(
            "/chat",
            {

            method:"POST",

            headers:
            {
                "Content-Type":
                "application/json"
            },


            body:
            JSON.stringify(
                {
                    question:question
                }
            )

            }
        );



        let data =
        await response.json();





        // ================================
        // Agent Trace
        // ================================


        let trace="";


        if(data.thoughts && data.thoughts.length){


            trace += `

            <div class="trace">

            <h3>
            🧠 Agent Trace
            </h3>


            <ul>

            ${
                data.thoughts.map(
                    step =>
                    `<li>${step}</li>`
                ).join("")
            }

            </ul>


            </div>

            `;


        }





        // ================================
        // Tools
        // ================================


        if(data.tools && data.tools.length){


            trace += `


            <div class="tools">


            <h3>
            🛠 Tools Used
            </h3>


            <p>

            ${
                data.tools.join(
                    " , "
                )
            }

            </p>


            </div>


            `;


        }




        // ================================
        // Routing
        // ================================


        if(data.routing){


            trace += `


            <div>

            <h3>
            🔀 Routing Decision
            </h3>


            <p>
            ${data.routing}
            </p>


            </div>


            `;


        }






        // ================================
        // Evidence Sections
        // ================================



        let evidence="";



        if(data.document){


            evidence += `


            <details>


            <summary>
            📄 Document Evidence
            </summary>


            <pre>
${data.document}
            </pre>


            </details>


            `;


        }





        if(data.wikipedia){


            evidence += `


            <details>


            <summary>
            🌐 Wikipedia Result
            </summary>


            <pre>
${data.wikipedia}
            </pre>


            </details>


            `;


        }






        if(data.tavily){


            evidence += `


            <details>


            <summary>
            🔎 Tavily Result
            </summary>


            <pre>
${data.tavily}
            </pre>


            </details>


            `;


        }







        // ================================
        // Final Answer
        // ================================


        let answer = `



        ${trace}



        <hr>


        <h2>
        💡 Answer
        </h2>


        <div class="answer-content">
        ${marked.parse(data.answer)}
        </div>



        <hr>



        <h3>
        📊 Metadata
        </h3>



        <p>

        <b>
        Source:
        </b>

        ${data.answer_source}


        <br>


        <b>
        Retrieval Score:
        </b>

        ${data.retrieval_score}


        <br>


        <b>
        Verified:
        </b>

        ${data.verified}


        <br>


        <b>
        Confidence:
        </b>

        ${data.confidence}



        </p>



        ${evidence}




        <details>


        <summary>
        ✅ Fact Check
        </summary>


        <p>
        ${data.verification}
        </p>


        </details>



        `;





        addMessage(
            answer,
            "bot"
        );



    }


    catch(error){


        console.log(error);


        addMessage(
            "❌ Server error",
            "bot"
        );


    }



}







// ======================================================
// Enter Key Support
// ======================================================


function handleEnter(event){


    if(event.key==="Enter"){

        askQuestion();

    }

}







// ======================================================
// Add Message To Chat
// ======================================================


// function addMessage(
//     text,
//     type
// ){



//     let chat =
//     document.getElementById(
//         "chat"
//     );



//     let div =
//     document.createElement(
//         "div"
//     );



//     div.className =
//     "message "+type;



//     div.innerHTML =
//     text;



//     chat.appendChild(
//         div
//     );



//     chat.scrollTop =
//     chat.scrollHeight;



// }


// ======================================================
// Add Message To Chat
// ======================================================

function addMessage(
    text,
    type
){

    let chat =
    document.getElementById(
        "chat"
    );


    let div =
    document.createElement(
        "div"
    );


    div.className =
    "message " + type;



    let avatar =
    type === "user"
    ? "👤"
    : "🤖";



    div.innerHTML =

    `

    <div class="avatar">

        ${avatar}

    </div>


    <div class="bubble">

        ${text}

    </div>

    `;



    chat.appendChild(
        div
    );


    chat.scrollTop =
    chat.scrollHeight;


}