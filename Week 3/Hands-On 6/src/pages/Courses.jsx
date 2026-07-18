import { useContext } from "react";

import { CourseContext } from "../context/CourseContext";

import CourseCard from "../components/CourseCard";

function Courses() {

    const { courseList } = useContext(CourseContext);

    return (

        <section className="page">

            <h2>Courses</h2>

            <div className="course-grid">

                {

                    courseList.map(course => (

                        <CourseCard

                            key={course.id}

                            course={course}

                        />

                    ))

                }

            </div>

        </section>

    );

}

export default Courses;
