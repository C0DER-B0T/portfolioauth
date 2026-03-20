
    st.markdown(f"""
    1. First **[Star the Public Repo](https://github.com/{PUBLIC_REPO})** ⭐
    2. Then **Login with [GitHub](https://github.com/)** to verify the star
    3. **Accept Invitation** to the Source Code Repo
    4. You will get a **new Repo Link** where all source code is available
    """)

[1] Why this works:

* st.expander: Provides the clickable header. When the user clicks "How To get Source code ❓", the list of steps drops down.
* Markdown Formatting: Using ** makes the key actions bold, making them easier to read at a glance.
* Dynamic Linking: The link in step 1 uses an f-string to automatically point to your PUBLIC_REPO variable.

Would you like to know how to integrate a GitHub Login button directly inside this expander for step 2?

[1] [https://stackoverflow.com](https://stackoverflow.com/questions/43407200/display-a-repository-of-which-i-am-collaborator-on-profile)
