import { createContext, useState } from "react";
import courses from "../data/courses";

export const CourseContext = createContext();

function CourseProvider({ children }) {

    const [courseList] = useState(courses);

    return (

        <CourseContext.Provider
            value={{ courseList }}
        >

            {children}

        </CourseContext.Provider>

    );

}

export default CourseProvider;
