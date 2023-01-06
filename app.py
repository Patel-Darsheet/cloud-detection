import streamlit as st
import requests


def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}


def main():
    st.set_page_config(page_title="CobraVision File Management",
                       page_icon="https://www.cobravision.ai/assets/img/logo-vertical.png")
    models = []
    dropdown = []
    # Call login_page function and store the return value in a variable
    login_success = login_page()
    # If login was successful, call the api_key_page function
    if login_success:
        api_key_submitted = api_key_page(models, dropdown)
        # If the API key was not successfully submitted, call the api_key_page function again
        while not api_key_submitted:
            api_key_submitted = api_key_page(models, dropdown)



def login_page():
    st.markdown(f'<style> body {{ background-color: #64a70b; }} </style>', unsafe_allow_html=True)
    st.markdown('<img src="https://www.cobravision.ai/assets/img/logo-vertical.png" width="200px">',
                unsafe_allow_html=True)
    st.markdown(f'<h1 style="color: #64a70b; text-align: center;">CobraVision File Management</h1>',
                unsafe_allow_html=True)
    with st.form("auth"):
        st.markdown(f'<h2 style="color: #64a70b; text-align: center;">Enter your login credentials:</h2>',
                    unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Submit")
        if submit:
            expected_username = "admin"
            expected_password = "CobraVision"
            if username == expected_username and password == expected_password:
                st.write("")  # Clear current page
                # Return True to indicate that login was successful
                return True
            else:
                st.error("Error - Incorrect username or password")
        # Return False to indicate that login was not successful
        return False


def api_key_page(models, dropdown):
    st.markdown(f'<style> body {{ background-color: #64a70b; }} </style>', unsafe_allow_html=True)
    st.markdown('<img src="https://www.cobravision.ai/assets/img/logo-vertical.png" width="200px">',
                unsafe_allow_html=True)
    st.markdown(f'<h1 style="color: #64a70b; text-align: center;">CobraVision File Management</h1>',
                unsafe_allow_html=True)
    with st.form("api_key"):
        st.markdown(f'<h2 style="color: #64a70b; text-align: center;">Enter your API key:</h2>',
                    unsafe_allow_html=True)
        api_key = st.text_input('API Key')
        submit = st.form_submit_button("Submit")

        if submit:
            st.write("Workspace Details")

            session = requests.Session()
            with st.spinner(text="Accessing workspace..."):
                data = fetch(session, f"https://api.roboflow.com/?api_key={api_key}")
                print(data)

            if "workspace" in data:
                st.success('Workspace found!', icon="✅")
                st.write(data)
                workspace = data["workspace"]
                if "workspace" in data and "projects" in data["workspace"]:
                    for project in data["workspace"]["projects"]:
                        identification = project["id"].split("/")[1]
                    print(identification)

                    data2 = fetch(session, f"https://api.roboflow.com/{workspace}/{identification}?api_key={api_key}")
                if "project" in data2 and "models" in data2["project"]:
                    for model in data2["project"]["models"]:
                        models.append(model)

                    dropdown = st.selectbox("Select a model", models)
                if workspace:
                    st.write("Projects")
                    with st.spinner(text="Parsing for model endpoints..."):
                        data = fetch(session, f"https://api.roboflow.com/{workspace}?api_key={api_key}")

                        if "workspace" in data and "projects" in data["workspace"]:
                            for project in data["workspace"]["projects"]:
                                identification = project["id"].split("/")[1]

                                data2 = fetch(session,
                                              f"https://api.roboflow.com/{workspace}/{identification}?api_key={api_key}")
                                if data2["versions"]:
                                    for version in data2["versions"]:
                                        if "model" in version:
                                            models.append(version["model"])

                            st.success('All projects parsed!', icon="✅")

                            for model in models:
                                identification = project["id"].split("/")[1]

                        data2 = fetch(session,
                                      f"https://api.roboflow.com/{workspace}/{identification}?api_key={api_key}")

                        if "project" in data2 and "models" in data2["project"]:
                            for model in data2["project"]["models"]:
                                models.append(model)

                            dropdown = st.selectbox("Select a model", models)

                if workspace:
                    st.write("Projects")
                    with st.spinner(text="Parsing for model endpoints..."):
                        data = fetch(session, f"https://api.roboflow.com/{workspace}?api_key={api_key}")

                        if "workspace" in data and "projects" in data["workspace"]:
                            for project in data["workspace"]["projects"]:
                                identification = project["id"].split("/")[1]

                                data2 = fetch(session,
                                              f"https://api.roboflow.com/{workspace}/{identification}?api_key={api_key}")
                                if data2["versions"]:
                                    for version in data2["versions"]:
                                        if "model" in version:
                                            models.append(version["model"])

                            st.success('All projects parsed!', icon="✅")

                            for model in models:
                                identification = model["id"]
                                map_score = model["map"]
                                dropdown.append(f"{identification} - mAP = {map_score}%")

                            option = st.selectbox(
                                'Models available for inference',
                                dropdown)

                        else:
                            st.error(
                                "Error - No projects found, double check you've created a project in your workspace")

                return True
            else:
                st.error("Error - double check API key")
                return False  # Return False to indicate that the API key was not successfully submitted

        # Return True to indicate that the API key was successfully submitted








if __name__ == '__main__':
    main()