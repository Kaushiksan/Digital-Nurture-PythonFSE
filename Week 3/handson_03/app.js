// ==========================================
// IMPORT COURSE DATA
// ==========================================

import { courses } from "./data.js";


// ==========================================
// ES6 DESTRUCTURING
// ==========================================

courses.forEach((course) => {

    const {
        name,
        credits
    } = course;

    console.log(
        `${name} has ${credits} credits`
    );

});


// ==========================================
// ARRAY MAP
// ==========================================

const formattedCourses = courses.map(
    ({
        code,
        name,
        credits
    }) => {

        return (
            `${code} — ${name} (${credits} credits)`
        );

    }
);

console.log(
    "Formatted Courses:",
    formattedCourses
);


// ==========================================
// ARRAY FILTER
// ==========================================

const highCreditCourses = courses.filter(
    (course) => course.credits >= 4
);

console.log(
    "Courses with 4 or more credits:",
    highCreditCourses
);

console.log(
    "High Credit Course Count:",
    highCreditCourses.length
);


// ==========================================
// ARRAY REDUCE
// ==========================================

const calculateTotalCredits = (
    courseList
) => {

    return courseList.reduce(
        (total, course) => {

            return total + course.credits;

        },
        0
    );

};


const totalCredits = calculateTotalCredits(
    courses
);

console.log(
    "Total Credits:",
    totalCredits
);


// ==========================================
// DOM SELECTION
// ==========================================

const courseGrid = document.querySelector(
    ".course-grid"
);

const totalCreditsElement =
    document.querySelector(
        "#total-credits"
    );

const searchInput =
    document.querySelector(
        "#search-courses"
    );

const sortButton =
    document.querySelector(
        "#sort-credits"
    );

const selectedCourse =
    document.querySelector(
        "#selected-course"
    );


// ==========================================
// RENDER COURSES
// ==========================================

const renderCourses = (
    courseList
) => {

    courseGrid.innerHTML = "";


    courseList.forEach(
        (course) => {

            const {
                id,
                name,
                code,
                credits
            } = course;


            const courseCard =
                document.createElement(
                    "article"
                );


            courseCard.className =
                "course-card";


            courseCard.dataset.id = id;


            courseCard.innerHTML = `

                <h3>
                    ${name}
                </h3>

                <p>
                    Course Code:
                    <strong>
                        ${code}
                    </strong>
                </p>

                <span>
                    ${credits} Credits
                </span>

            `;


            courseGrid.appendChild(
                courseCard
            );

        }
    );


    totalCreditsElement.textContent =
        `Total Credits: ${
            calculateTotalCredits(
                courseList
            )
        }`;

};


// ==========================================
// INITIAL COURSE RENDER
// ==========================================

renderCourses(courses);


// ==========================================
// SEARCH COURSES
// ==========================================

searchInput.addEventListener(
    "input",
    (event) => {

        const searchText =
            event.target.value
                .toLowerCase();


        const filteredCourses =
            courses.filter(
                (course) => {

                    return course.name
                        .toLowerCase()
                        .includes(
                            searchText
                        );

                }
            );


        renderCourses(
            filteredCourses
        );

    }
);


// ==========================================
// SORT COURSES BY CREDITS
// ==========================================

sortButton.addEventListener(
    "click",
    () => {

        courses.sort(
            (firstCourse, secondCourse) => {

                return (
                    secondCourse.credits
                    - firstCourse.credits
                );

            }
        );


        renderCourses(courses);

    }
);


// ==========================================
// EVENT DELEGATION
// ==========================================

courseGrid.addEventListener(
    "click",
    (event) => {

        const courseCard =
            event.target.closest(
                ".course-card"
            );


        if (!courseCard) {

            return;

        }


        const courseId = Number(
            courseCard.dataset.id
        );


        const course = courses.find(
            (course) => {

                return (
                    course.id === courseId
                );

            }
        );


        if (!course) {

            return;

        }


        selectedCourse.textContent =
            `Selected Course: ${
                course.name
            } | Grade: ${
                course.grade
            }`;

    }
);
