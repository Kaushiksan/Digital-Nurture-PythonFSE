import {
    useEffect,
    useState
} from "react";


import Header from "./components/Header";

import Footer from "./components/Footer";

import CourseCard from "./components/CourseCard";

import StudentProfile from "./components/StudentProfile";


import "./App.css";


function App() {

    // ======================================
    // COURSE STATE
    // ======================================

    const [
        courses,
        setCourses
    ] = useState([]);


    // ======================================
    // SEARCH STATE
    // ======================================

    const [
        searchTerm,
        setSearchTerm
    ] = useState("");


    // ======================================
    // ENROLLED COURSES STATE
    // ======================================

    const [
        enrolledCourses,
        setEnrolledCourses
    ] = useState([]);


    // ======================================
    // LOADING STATE
    // ======================================

    const [
        loading,
        setLoading
    ] = useState(true);


    // ======================================
    // ERROR STATE
    // ======================================

    const [
        error,
        setError
    ] = useState("");


    // ======================================
    // FETCH COURSES
    // ======================================

    useEffect(() => {

        const fetchCourses = async () => {

            try {

                setLoading(true);


                const response = await fetch(

                    "https://jsonplaceholder.typicode.com/posts?_limit=5"

                );


                if (!response.ok) {

                    throw new Error(
                        "Unable to fetch courses"
                    );

                }


                const posts =
                    await response.json();


                const courseData = posts.map(

                    (post, index) => ({

                        id: post.id,

                        name: post.title,

                        code: `CS10${index + 1}`,

                        credits:
                            index % 2 === 0
                                ? 4
                                : 3,

                        grade:
                            index % 2 === 0
                                ? "A"
                                : "B+"

                    })

                );


                setCourses(
                    courseData
                );


                setError("");

            }
            catch (fetchError) {

                setError(
                    "Failed to load courses."
                );

            }
            finally {

                setLoading(false);

            }

        };


        fetchCourses();

    }, []);


    // ======================================
    // COURSES UPDATED EFFECT
    // ======================================

    useEffect(() => {

        console.log(
            "Courses updated"
        );

        /*
        The dependency array contains courses.

        This effect runs whenever the courses
        state changes.

        Without a dependency array, the effect
        would run after every render.
        */

    }, [courses]);


    // ======================================
    // ENROLL COURSE
    // ======================================

    const handleEnroll = (
        courseId
    ) => {

        const selectedCourse =
            courses.find(

                (course) =>
                    course.id === courseId

            );


        if (!selectedCourse) {

            return;

        }


        const alreadyEnrolled =
            enrolledCourses.some(

                (course) =>
                    course.id === courseId

            );


        if (alreadyEnrolled) {

            return;

        }


        setEnrolledCourses(

            (previousCourses) => [

                ...previousCourses,

                selectedCourse

            ]

        );

    };


    // ======================================
    // FILTER COURSES
    // ======================================

    const filteredCourses =
        courses.filter(

            (course) => {

                return course.name
                    .toLowerCase()
                    .includes(
                        searchTerm.toLowerCase()
                    );

            }

        );


    // ======================================
    // JSX
    // ======================================

    return (

        <>

            <Header
                siteName="Student Portal"
                enrolledCount={
                    enrolledCourses.length
                }
            />


            <main>

                <section
                    id="home"
                    className="hero"
                >

                    <h2>
                        Welcome to Student Portal
                    </h2>

                    <p>
                        Manage courses and student
                        information using React.
                    </p>

                </section>


                <section
                    id="courses"
                    className="courses-section"
                >

                    <h2>
                        My Courses
                    </h2>


                    <input
                        className="search-input"
                        type="text"
                        placeholder="Search courses..."
                        value={searchTerm}
                        onChange={
                            (event) => {

                                setSearchTerm(
                                    event.target.value
                                );

                            }
                        }
                    />


                    {
                        loading && (

                            <p className="status-message">

                                Loading...

                            </p>

                        )
                    }


                    {
                        error && (

                            <p className="error-message">

                                {error}

                            </p>

                        )
                    }


                    {
                        !loading && !error && (

                            <div className="course-grid">

                                {
                                    filteredCourses.map(

                                        (course) => (

                                            <CourseCard
                                                key={course.id}
                                                {...course}
                                                onEnroll={
                                                    handleEnroll
                                                }
                                            />

                                        )

                                    )
                                }

                            </div>

                        )
                    }


                    {
                        !loading
                        && !error
                        && filteredCourses.length === 0
                        && (

                            <p className="status-message">

                                No courses found.

                            </p>

                        )
                    }

                </section>


                <StudentProfile />

            </main>


            <Footer />

        </>

    );

}


export default App;
