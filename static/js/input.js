let educationCounter = 0;
let skillsCounter = 0;
let coursesCounter = 0;
let languagesCounter = 0;
let internshipsCounter = 0;
let projectsCounter = 0;
function createDeleteButton(parentDiv) {
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.classList.add("delete-btn");
    deleteBtn.onclick = function () {
      parentDiv.remove();
    };
    return deleteBtn;
  }

  // Add dynamic education fields
  function addEducation() {
    educationCounter++; 
    const educationSection = document.getElementById("education-section");
    const div = document.createElement("div");
    div.classList.add("education-entry");
    div.innerHTML = `
        <label>Degree:</label>
        <input type="text" name="degree_${educationCounter}" placeholder="Enter your degree"><br>
        <label>Institution:</label>
        <input type="text" name="institution_${educationCounter}" placeholder="Enter the institution"><br>
        <label>Date:</label>
        <input type="text" name="date_${educationCounter}" placeholder="Enter the dates"><br><br>
    `;
    const deleteBtn = createDeleteButton(div);
    div.appendChild(deleteBtn);
    educationSection.appendChild(div);
  
    document.getElementById("educationCounter").value = educationCounter;
}

  // Add dynamic skills fields
  function addSkill() {
    const skillsSection = document.getElementById("skills-section");
    const div = document.createElement("div");
    div.classList.add("skill-entry");
    div.innerHTML = `
          <input type="text" placeholder="Enter your skill"><br><br>
      `;
    const deleteBtn = createDeleteButton(div); // Create delete button
    div.appendChild(deleteBtn);
    skillsSection.appendChild(div);
  }

  // Add dynamic course section
  function addCourses() {
    const dynamicSection = document.getElementById("dynamic-sections");
    const div = document.createElement("div");
    div.classList.add("course-entry");
    div.innerHTML = `
          <h4>Courses</h4>
          <label>Course Name:</label>
          <input type="text" placeholder="Enter course name"><br>
          <label>Institution:</label>
          <input type="text" placeholder="Enter institution"><br>
          <label>Date:</label>
          <input type="text" placeholder="Enter completion date"><br><br>
      `;
    const deleteBtn = createDeleteButton(div); // Create delete button
    div.appendChild(deleteBtn);
    dynamicSection.appendChild(div);
  }

  // Add dynamic languages section
  function addLanguages() {
    const dynamicSection = document.getElementById("dynamic-sections");
    const div = document.createElement("div");
    div.classList.add("language-entry");
    div.innerHTML = `
          <h4>Languages</h4>
          <label>Language:</label>
          <input type="text" placeholder="Enter language"><br>
          <label>Proficiency:</label>
          <input type="text" placeholder="Enter proficiency (e.g., fluent, basic)"><br><br>
      `;
    const deleteBtn = createDeleteButton(div); // Create delete button
    div.appendChild(deleteBtn);
    // deleteBtn.className("btn")
    dynamicSection.appendChild(div);
  }

  // Add dynamic internships section
  function addInternships() {
    const dynamicSection = document.getElementById("dynamic-sections");
    const div = document.createElement("div");
    div.classList.add("internship-entry");
    div.innerHTML = `
          <h4>Internships</h4>
          <label>Company:</label>
          <input type="text" placeholder="Enter company name"><br>
          <label>Role:</label>
          <input type="text" placeholder="Enter role"><br>
          <label>Date:</label>
          <input type="text" placeholder="Enter internship dates"><br><br>
      `;
    const deleteBtn = createDeleteButton(div); // Create delete button
    div.appendChild(deleteBtn);
    dynamicSection.appendChild(div);
  }

  function addProjects() {
    const dynamicSection = document.getElementById("dynamic-sections");
    const div = document.createElement("div");
    div.classList.add("project-entry");
    div.innerHTML = `
          <h4>Projects</h4>
          <label>Project Name:</label>
          <input type="text" placeholder="Enter Project name here"><br>
          <label>Description</label>
          <input type="text" placeholder="Enter Project description"><br>
      `;
    const deleteBtn = createDeleteButton(div); // Create delete button
    div.appendChild(deleteBtn);
    dynamicSection.appendChild(div);
  }