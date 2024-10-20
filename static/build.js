// This function handles form submission to generate the resume
document.addEventListener('DOMContentLoaded', () => {
    const downloadSection = document.getElementById("downloadSection");
    const downloadDocxButton = document.getElementById("docxDownload");
    const downloadPdfButton = document.getElementById("pdfDownload");
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    // let existingDiv = document.getElementById(selectedValue + 'Fields');

    // Handle form submission
    document.querySelector(".button_clk").addEventListener("click", async function (e) {
        alert("data error")
        e.preventDefault(); // Prevent the default form submission
        const formData = new FormData(document.querySelector("form"));
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });
        console.log(data)

        try {
            const response = await fetch("/resumes/generate/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,

                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const fileUrls = await response.json(); // Expecting JSON response with file URLs

            // Show the download links
            downloadDocxButton.href = `/media/${fileUrls.docx_url}`;
            downloadPdfButton.href = `/media/${fileUrls.pdf_url}`;
            downloadSection.style.display = 'block';
        } catch (error) {
            alert('Failed to generate the resume. Please try again.');
            console.error("Error:", error);
        }
    });
    
        // Add input fields based on the checkbox selected, only if they don't already exist
        // if (!existingDiv) { // Only create if not already created
        //     if (selectedValue === 'certifications') {
        //         const certDiv = document.createElement('div');
        //         certDiv.id = 'certificationsFields';
        //         certDiv.innerHTML = `
        //             <label>How many certificates?</label><br>
        //             <input type="number" name="certificateCount" min="1" max="10" value="1"><br><br>
        //             <label>Add your certifications:</label><br>
        //             <textarea name="certifications" rows="4" cols="50" placeholder="List your certifications"></textarea><br><br>
        //         `;
        //         additionalFieldsDiv.appendChild(certDiv);
        //     } else if (selectedValue === 'leadership') {
        //         const leadershipDiv = document.createElement('div');
        //         leadershipDiv.id = 'leadershipFields';
        //         leadershipDiv.innerHTML = `
        //             <label>How many leadership skills?</label><br>
        //             <input type="number" name="leadershipCount" min="1" max="10" value="1"><br><br>
        //             <label>Describe your leadership skills:</label><br>
        //             <textarea name="leadershipSkills" rows="4" cols="50" placeholder="Describe your leadership skills"></textarea><br><br>
        //         `;
        //         additionalFieldsDiv.appendChild(leadershipDiv);
        //     } else if (selectedValue === 'experience') {
        //         const experienceDiv = document.createElement('div');
        //         experienceDiv.id = 'experienceFields';
        //         experienceDiv.innerHTML = `
        //             <label>How many years of experience?</label><br>
        //             <input type="number" name="experienceYears" min="1" max="50" value="1"><br><br>
        //             <label>Describe your experience:</label><br>
        //             <textarea name="experienceDescription" rows="4" cols="50" placeholder="Describe your experience"></textarea><br><br>
        //         `;
        //         additionalFieldsDiv.appendChild(experienceDiv);
        //     }
        // }
    });
    
