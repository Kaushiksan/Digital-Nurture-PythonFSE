// ==========================================
// IMPORT LOCAL DATA
// ==========================================

import { courses } from "./data.js";


// ==========================================
// API CONFIGURATION
// ==========================================

const API_URL =
    "https://jsonplaceholder.typicode.com";


// ==========================================
// DOM ELEMENTS
// ==========================================

const courseGrid =
    document.querySelector(
        ".course-grid"
    );

const courseStatus =
    document.querySelector(
        "#course-status"
    );

const notificationGrid =
    document.querySelector(
        ".notification-grid"
    );

const notificationStatus =
    document.querySelector(
        "#notification-status"
    );

const notificationLoading =
    document.querySelector(
        "#notification-loading"
    );

const retryButton =
    document.querySelector(
        "#retry-button"
    );

const errorMessage =
    document.querySelector(
        "#error-message"
    );

const errorRetryButton =
    document.querySelector(
        "#error-retry-button"
    );


// ==========================================
// TASK 1
// PROMISE CHAINING
// ==========================================

const fetchUser = (id) => {

    return fetch(
        `${API_URL}/users/${id}`
    );

};


fetchUser(1)

    .then((response) => {

        return response.json();

    })

    .then((user) => {

        console.log(
            "Promise User:",
            user.name
        );

    })

    .catch((error) => {

        console.error(
            "Promise Error:",
            error
        );

    });


// ==========================================
// ASYNC / AWAIT VERSION
// ==========================================

const fetchUserAsync = async (id) => {

    try {

        const response = await fetch(
            `${API_URL}/users/${id}`
        );


        if (!response.ok) {

            throw new Error(
                `HTTP Error: ${response.status}`
            );

        }


        const user = await response.json();


        console.log(
            "Async User:",
            user.name
        );


        return user;

    }
    catch (error) {

        console.error(
            "Async User Error:",
            error.message
        );

        throw error;

    }

};


fetchUserAsync(1);


// ==========================================
// SIMULATED COURSE API
// ==========================================

const fetchAllCourses = async () => {

    await new Promise(
        (resolve) => {

            setTimeout(
                resolve,
                1000
            );

        }
    );


    return courses;

};


// ==========================================
// RENDER COURSES
// ==========================================

const renderCourses = (
    courseList
) => {

    courseGrid.innerHTML = "";


    courseList.forEach(
        (course) => {

            const article =
                document.createElement(
                    "article"
                );


            article.className =
                "course-card";


            article.innerHTML = `

                <h3>
                    ${course.name}
                </h3>

                <p>
                    ${course.code}
                </p>

                <strong>
                    ${course.credits} Credits
                </strong>

            `;


            courseGrid.appendChild(
                article
            );

        }
    );

};


// ==========================================
// LOAD COURSES
// ==========================================

const loadCourses = async () => {

    courseStatus.textContent =
        "Loading courses...";


    courseGrid.innerHTML = "";


    try {

        const courseList =
            await fetchAllCourses();


        renderCourses(
            courseList
        );


        courseStatus.textContent =
            "Courses loaded successfully.";

    }
    catch (error) {

        courseStatus.textContent =
            "Unable to load courses.";

    }

};


loadCourses();


// ==========================================
// PROMISE.ALL DEMONSTRATION
// ==========================================

const loadMultipleUsers = async () => {

    try {

        const [
            firstUser,
            secondUser
        ] = await Promise.all([

            fetchUserAsync(1),

            fetchUserAsync(2)

        ]);


        console.log(
            "Promise.all Users:",
            firstUser.name,
            secondUser.name
        );

    }
    catch (error) {

        console.error(
            "Unable to load users."
        );

    }

};


loadMultipleUsers();


// ==========================================
// TASK 2
// REUSABLE FETCH FUNCTION
// ==========================================

const apiFetch = async (url) => {

    const response = await fetch(url);


    if (!response.ok) {

        throw new Error(
            `Request failed with status ${response.status}`
        );

    }


    return response.json();

};


// ==========================================
// RENDER NOTIFICATIONS
// ==========================================

const renderNotifications = (
    posts
) => {

    notificationGrid.innerHTML = "";


    posts.forEach(
        (post) => {

            const notification =
                document.createElement(
                    "article"
                );


            notification.className =
                "notification-card";


            notification.innerHTML = `

                <h3>
                    ${post.title}
                </h3>

                <p>
                    ${post.body}
                </p>

            `;


            notificationGrid.appendChild(
                notification
            );

        }
    );

};


// ==========================================
// LOAD NOTIFICATIONS
// ==========================================

const loadNotifications = async () => {

    notificationGrid.innerHTML = "";

    notificationStatus.textContent = "";

    retryButton.hidden = true;

    notificationLoading.classList.add(
        "show"
    );


    try {

        const posts = await apiFetch(
            `${API_URL}/posts?_limit=6`
        );


        renderNotifications(
            posts
        );


        notificationStatus.textContent =
            "Notifications loaded successfully.";

    }
    catch (error) {

        notificationStatus.textContent =
            "Unable to load notifications. Please try again.";


        retryButton.hidden = false;

    }
    finally {

        notificationLoading.classList.remove(
            "show"
        );

    }

};


loadNotifications();


// ==========================================
// RETRY NOTIFICATIONS
// ==========================================

retryButton.addEventListener(
    "click",
    loadNotifications
);


// ==========================================
// SIMULATE 404 ERROR
// ==========================================

const demonstrateError = async () => {

    errorMessage.textContent =
        "Checking invalid API endpoint...";


    errorRetryButton.hidden = true;


    try {

        await apiFetch(
            `${API_URL}/nonexistent`
        );


        errorMessage.textContent =
            "Request completed.";

    }
    catch (error) {

        errorMessage.textContent =
            "The requested API resource could not be found.";


        errorRetryButton.hidden = false;

    }

};


demonstrateError();


// ==========================================
// ERROR RETRY
// ==========================================

errorRetryButton.addEventListener(
    "click",
    async () => {

        errorMessage.textContent =
            "Retrying with a valid endpoint...";


        errorRetryButton.hidden = true;


        try {

            const posts = await apiFetch(
                `${API_URL}/posts?_limit=6`
            );


            renderNotifications(
                posts
            );


            errorMessage.textContent =
                "Retry successful. Notifications loaded.";

        }
        catch (error) {

            errorMessage.textContent =
                "Retry failed. Please try again.";

            errorRetryButton.hidden = false;

        }

    }
);


// ==========================================
// TASK 3
// AXIOS REQUEST INTERCEPTOR
// ==========================================

axios.interceptors.request.use(
    (config) => {

        console.log(
            `API call started: ${config.url}`
        );


        return config;

    },

    (error) => {

        return Promise.reject(
            error
        );

    }
);


// ==========================================
// AXIOS API FUNCTION
// ==========================================

const axiosFetch = async (url) => {

    const response = await axios.get(
        url
    );


    return response.data;

};


// ==========================================
// AXIOS PARAMS EXAMPLE
// ==========================================

const loadUserOnePosts = async () => {

    try {

        const response = await axios.get(
            `${API_URL}/posts`,
            {
                params: {
                    userId: 1
                }
            }
        );


        console.log(
            "Axios User 1 Posts:",
            response.data
        );

    }
    catch (error) {

        console.error(
            "Axios Error:",
            error.message
        );

    }

};


loadUserOnePosts();


// ==========================================
// AXIOS FETCH EXAMPLE
// ==========================================

const testAxiosFetch = async () => {

    try {

        const user = await axiosFetch(
            `${API_URL}/users/1`
        );


        console.log(
            "Axios User:",
            user.name
        );

    }
    catch (error) {

        console.error(
            "Axios Fetch Error:",
            error.message
        );

    }

};


testAxiosFetch();


// ==========================================
// FETCH VS AXIOS
// ==========================================

/*

FETCH VS AXIOS

1. Fetch is built into modern browsers.
   Axios is an external JavaScript library.

2. Fetch requires response.json() to parse JSON.
   Axios automatically parses JSON and provides
   the result in response.data.

3. Fetch does not reject automatically for HTTP
   errors such as 404 and 500. response.ok must
   be checked manually.

   Axios rejects non-2xx HTTP responses by default.

*/
