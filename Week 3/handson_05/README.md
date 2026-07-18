# Hands-On 5 – React Fundamentals

## Objective

Rebuild the Student Portal using React and learn JSX, functional components, props, state and React Hooks.

## Topics Covered

- JSX
- Functional Components
- Props
- useState
- useEffect
- Conditional Rendering
- Dynamic Lists
- Controlled Inputs
- Lifting State Up

## Project Structure

```text
handson_05/
├── src/
│   ├── components/
│   │   ├── CourseCard.jsx
│   │   ├── Footer.jsx
│   │   ├── Header.jsx
│   │   └── StudentProfile.jsx
│   ├── App.css
│   ├── App.jsx
│   ├── index.css
│   └── main.jsx
├── index.html
├── package.json
└── README.md
```

## Components

### Header

Displays:

- Student Portal site name
- Navigation links
- Enrolled course count

### CourseCard

Displays:

- Course name
- Course code
- Credits
- Grade
- Enroll button

### StudentProfile

Contains local state for:

- Name
- Email
- Semester

## React State

The application uses `useState` for:

- Courses
- Search term
- Enrolled courses
- Loading state
- Error state

## Course API

Course data is loaded from JSONPlaceholder.

The first five posts are mapped into course-like objects.

## useEffect

One effect fetches courses when the application mounts.

Another effect logs:

```text
Courses updated
```

whenever the courses state changes.

## Search

Typing in the search field filters the displayed course cards in real time.

## Enrolment

Clicking the Enroll button adds a course to the enrolled courses state.

The enrolled course count is displayed in the Header.

## Run Project

```bash
npm install
npm run dev
```

## Expected Outcome

- React application runs successfully.
- Header and Footer render.
- CourseCard components render dynamically.
- Courses load from an API.
- Loading state is displayed.
- Errors are handled.
- Search filters courses.
- Enroll updates the enrolled course count.
- Student profile form updates local state.

## Status

Completed
