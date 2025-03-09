import streamlit as st
from datetime import datetime
import re
import json
import os

# Initialize session state for persistent data
if 'data_initialized' not in st.session_state:
    st.session_state.data_initialized = True
    
    # Load data from file if exists, otherwise use defaults
    data_file = "filename_generator_data.json"
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
            st.session_state.project_years = data.get('project_years', ['CE23', 'CE24', 'CE25', 'CE26'])
            st.session_state.city_codes = data.get('city_codes', ['BKR', 'SDT', 'CAI', 'GIZ', 'ALX', 'SSH', 'LXR', 'ASW', 'ISM', 'FYM', 'SHG', 'AST', 'MAN', 'ZAG', 'PSD', 'BSF', 'QEN', 'SUE', 'MIN', 'DAM', 'DKH', 'MNF', 'QLY', 'KES', 'MTH', 'RED', 'SHQ', 'OCT', 'RAM', 'NCA'])
            st.session_state.disciplines = data.get('disciplines', {'STR': 'Structural', 'ARC': 'Architectural', 'ELE': 'Electrical', 'MEC': 'Mechanical', 'ENV': 'Environmental', 'CIV': 'Civil', 'GEO': 'Geotechnical', 'HYD': 'Hydraulic', 'SAN': 'Sanitary'})
            st.session_state.doc_types = data.get('doc_types', {'D': 'Drawing', 'C': 'Calculation', 'R': 'Report', 'SP': 'Specification', 'MOM': 'Minutes of Meeting', 'LTR': 'Letter'})
            st.session_state.elements = data.get('elements', {'WTP': 'Water Treatment Plant', 'WWTP': 'Wastewater Treatment Plant', 'PST': 'Pump Station', 'RWS': 'Raw Water Sump', 'PWS': 'Pure Water Sump', 'FB': 'Filter Building', 'CF': 'Clariflocculator', 'CHL': 'Chlorine Building', 'GEN': 'Generator', 'TRF': 'Transformer', 'NET': 'Network', 'GRD': 'Ground Tank', 'OVT': 'Elevated Storage Tank', 'INT': 'Intake', 'ADM': 'Admin Building', 'SLD': 'Sanitary Landfill', 'TS': 'Transfer Station', 'SWM': 'Solid Waste Management'})
            st.session_state.revisions = data.get('revisions', ['A', 'B', 'C', 'D'])
            st.session_state.file_extensions = data.get('file_extensions', ['pdf', 'xlsx', 'docx', 'dwg', 'jpg'])
            st.session_state.companies = data.get('companies', {'CMCT': 'Client Company', 'VNCL': 'Vendor Company', 'SBCT': 'Subcontractor'})
            st.session_state.letter_registry = data.get('letter_registry', [])
    else:
        # Default values
        st.session_state.project_years = ['CE23', 'CE24', 'CE25', 'CE26']
        st.session_state.city_codes = ['BKR', 'SDT', 'CAI', 'GIZ', 'ALX', 'SSH', 'LXR', 'ASW', 'ISM', 'FYM', 'SHG', 'AST', 'MAN', 'ZAG', 'PSD', 'BSF', 'QEN', 'SUE', 'MIN', 'DAM', 'DKH', 'MNF', 'QLY', 'KES', 'MTH', 'RED', 'SHQ', 'OCT', 'RAM', 'NCA']
        st.session_state.disciplines = {'STR': 'Structural', 'ARC': 'Architectural', 'ELE': 'Electrical', 'MEC': 'Mechanical', 'ENV': 'Environmental', 'CIV': 'Civil', 'GEO': 'Geotechnical', 'HYD': 'Hydraulic', 'SAN': 'Sanitary'}
        st.session_state.doc_types = {'D': 'Drawing', 'C': 'Calculation', 'R': 'Report', 'SP': 'Specification', 'MOM': 'Minutes of Meeting', 'LTR': 'Letter'}
        st.session_state.elements = {'WTP': 'Water Treatment Plant', 'WWTP': 'Wastewater Treatment Plant', 'PST': 'Pump Station', 'RWS': 'Raw Water Sump', 'PWS': 'Pure Water Sump', 'FB': 'Filter Building', 'CF': 'Clariflocculator', 'CHL': 'Chlorine Building', 'GEN': 'Generator', 'TRF': 'Transformer', 'NET': 'Network', 'GRD': 'Ground Tank', 'OVT': 'Elevated Storage Tank', 'INT': 'Intake', 'ADM': 'Admin Building', 'SLD': 'Sanitary Landfill', 'TS': 'Transfer Station', 'SWM': 'Solid Waste Management'}
        st.session_state.revisions = ['A', 'B', 'C', 'D']
        st.session_state.file_extensions = ['pdf', 'xlsx', 'docx', 'dwg', 'jpg']
        st.session_state.companies = {'CMCT': 'Client Company', 'VNCL': 'Vendor Company', 'SBCT': 'Subcontractor'}
        st.session_state.letter_registry = []

# Function to save data
def save_data():
    data = {
        'project_years': st.session_state.project_years,
        'city_codes': st.session_state.city_codes,
        'disciplines': st.session_state.disciplines,
        'doc_types': st.session_state.doc_types,
        'elements': st.session_state.elements,
        'revisions': st.session_state.revisions,
        'file_extensions': st.session_state.file_extensions,
        'companies': st.session_state.companies,
        'letter_registry': st.session_state.letter_registry
    }
    with open("filename_generator_data.json", 'w') as f:
        json.dump(data, f, indent=4)
    st.success("Data saved successfully!")

# Function to validate project number
def validate_project_number(num):
    pattern = r'^\d+$'
    if re.match(pattern, num):
        return True
    return False

# Function to register a letter
def register_letter(filename, direction, company, subject, has_attachments, attachments):
    letter_entry = {
        'filename': filename,
        'date': datetime.today().strftime("%Y-%m-%d"),
        'direction': direction,
        'company': company,
        'company_name': st.session_state.companies.get(company, "Unknown"),
        'subject': subject,
        'has_attachments': has_attachments,
        'attachments': attachments
    }
    st.session_state.letter_registry.append(letter_entry)
    save_data()
    return letter_entry

# Set page config
st.set_page_config(page_title="Document Filename Generator", page_icon="📄", layout="wide")

# App title and description
st.title("Document Filename Generator")
st.markdown("""
This tool generates standardized filenames for engineering project documents based on your inputs.
The format is: `[Project Year]-[City][Project Number]-[Discipline]-[Doc Type]-[Element]-[Revision].[Extension]`
""")

# Create tabs for generator, letters, and management
tab1, tab2, tab3, tab4 = st.tabs(["Generator", "Letter Management", "Data Management", "Help"])

with tab1:
    # User inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Project Information")
        project_year = st.selectbox('Project Year', st.session_state.project_years)
        city = st.selectbox("City", st.session_state.city_codes)
        project_number = st.text_input('Project Number (e.g., 1, 2, 3...)', '1')
        
        # Validate project number
        if project_number and not validate_project_number(project_number):
            st.error("Project number must contain only digits")
            
    with col2:
        st.subheader("Document Information")
        discipline = st.selectbox("Discipline", list(st.session_state.disciplines.keys()), 
                               format_func=lambda x: f"{x} - {st.session_state.disciplines[x]}")
        doc_type = st.selectbox("Document Type", list(st.session_state.doc_types.keys()), 
                             format_func=lambda x: f"{x} - {st.session_state.doc_types[x]}")
        element = st.selectbox("Element", list(st.session_state.elements.keys()), 
                            format_func=lambda x: f"{x} - {st.session_state.elements[x]}")
        
    with col3:
        st.subheader("Version Information")
        revision = st.selectbox("Revision", st.session_state.revisions)
        file_ext = st.selectbox("File Extension", st.session_state.file_extensions)
        date = st.date_input("Document Date", datetime.today())
        date_str = date.strftime("%Y-%m-%d")
    
    # Letter-specific inputs (conditional)
    if doc_type == "LTR":
        st.subheader("Letter Information")
        letter_cols = st.columns(3)
        with letter_cols[0]:
            letter_direction = st.radio("Letter Direction", ["Incoming", "Outgoing"])
        with letter_cols[1]:
            letter_company = st.selectbox("Company", list(st.session_state.companies.keys()),
                                      format_func=lambda x: f"{x} - {st.session_state.companies[x]}")
        with letter_cols[2]:
            letter_subject = st.text_input("Subject")
        
        has_attachments = st.checkbox("Has Attachments")
        if has_attachments:
            attachment_list = st.text_area("List Attachments (one per line)")
            attachments = [a.strip() for a in attachment_list.split('\n') if a.strip()]
        else:
            attachments = []
    
    # Preview section
    st.subheader("Filename Preview")
    if validate_project_number(project_number):
        filename = f"{project_year}-{city}{project_number}-{discipline}-{doc_type}-{element}-{revision}.{file_ext}"
        
        # Display preview with parts highlighted
        col1, col2 = st.columns([3, 1])
        with col1:
            st.code(filename)
            
        with col2:
            # Using Streamlit's built-in functionality for text selection
            st.text_input("Copy this filename:", value=filename, key="filename_input", label_visibility="collapsed")
            st.caption("👆 Click to select, then copy (Ctrl+C/Cmd+C)")
        
        # Generate Button
        if st.button("Generate Document"):
            # Basic filename generation
            st.success(f"✅ Generated: {filename}")
            
            # Additional letter registration if applicable
            if doc_type == "LTR":
                letter_entry = register_letter(
                    filename,
                    letter_direction,
                    letter_company,
                    letter_subject,
                    has_attachments,
                    attachments
                )
                st.info(f"Letter registered: {letter_direction} from/to {letter_entry['company_name']}")
                if has_attachments:
                    st.info(f"With {len(attachments)} attachments")
        
        # Show breakdown of filename parts
        st.subheader("Filename Breakdown")
        breakdown = {
            "Project Year": f"{project_year}",
            "Location": f"{city}",
            "Project Number": f"{project_number}",
            "Discipline": f"{discipline} ({st.session_state.disciplines[discipline]})",
            "Document Type": f"{doc_type} ({st.session_state.doc_types[doc_type]})",
            "Element": f"{element} ({st.session_state.elements[element]})",
            "Revision": f"{revision}",
            "File Extension": f"{file_ext}",
            "Date Created": f"{date_str}"
        }
        
        for key, value in breakdown.items():
            st.write(f"**{key}:** {value}")
            
        # Additional metadata
        with st.expander("Additional Metadata"):
            st.write(f"**Full Document Name:** {st.session_state.doc_types[doc_type]} for {st.session_state.elements[element]}")
            st.write(f"**Created On:** {date_str}")
            st.write(f"**Document Path:** /projects/{project_year}/{city}{project_number}/{discipline}/{filename}")

with tab2:
    st.header("Letter Management")
    
    # Letter registry
    st.subheader("Letter Registry")
    if not st.session_state.letter_registry:
        st.info("No letters registered yet. Create a letter document (LTR) to add to the registry.")
    else:
        # Filter options
        filter_cols = st.columns(4)
        with filter_cols[0]:
            filter_direction = st.selectbox("Filter by Direction", ["All", "Incoming", "Outgoing"])
        with filter_cols[1]:
            filter_company = st.selectbox("Filter by Company", ["All"] + list(st.session_state.companies.keys()))
        with filter_cols[2]:
            filter_has_attachments = st.selectbox("Filter by Attachments", ["All", "With Attachments", "Without Attachments"])
        with filter_cols[3]:
            sort_by = st.selectbox("Sort by", ["Date (newest first)", "Date (oldest first)", "Company"])
        
        # Apply filters
        filtered_letters = st.session_state.letter_registry.copy()
        if filter_direction != "All":
            filtered_letters = [l for l in filtered_letters if l['direction'] == filter_direction]
        if filter_company != "All":
            filtered_letters = [l for l in filtered_letters if l['company'] == filter_company]
        if filter_has_attachments != "All":
            if filter_has_attachments == "With Attachments":
                filtered_letters = [l for l in filtered_letters if l['has_attachments']]
            else:
                filtered_letters = [l for l in filtered_letters if not l['has_attachments']]
        
        # Apply sorting
        if sort_by == "Date (newest first)":
            filtered_letters = sorted(filtered_letters, key=lambda x: x['date'], reverse=True)
        elif sort_by == "Date (oldest first)":
            filtered_letters = sorted(filtered_letters, key=lambda x: x['date'])
        elif sort_by == "Company":
            filtered_letters = sorted(filtered_letters, key=lambda x: x['company_name'])
        
        # Display letters
        for i, letter in enumerate(filtered_letters):
            with st.expander(f"{letter['date']} - {letter['direction']} - {letter['company_name']} - {letter['subject']}"):
                st.write(f"**Filename:** {letter['filename']}")
                st.write(f"**Direction:** {letter['direction']}")
                st.write(f"**Company:** {letter['company_name']} ({letter['company']})")
                st.write(f"**Subject:** {letter['subject']}")
                st.write(f"**Date:** {letter['date']}")
                
                if letter['has_attachments']:
                    st.write("**Attachments:**")
                    for attachment in letter['attachments']:
                        st.write(f"- {attachment}")
                else:
                    st.write("**No attachments**")
                
                # Delete button
                if st.button("Delete Letter", key=f"delete_{i}"):
                    st.session_state.letter_registry.remove(letter)
                    save_data()
                    st.experimental_rerun()

with tab3:
    st.header("Data Management")
    
    manage_tab1, manage_tab2, manage_tab3, manage_tab4, manage_tab5, manage_tab6 = st.tabs([
        "Project Years", "City Codes", "Disciplines", "Document Types", "Elements", "Companies"
    ])
    
    with manage_tab1:
        st.subheader("Manage Project Years")
        years_text = st.text_area("Project Years (one per line)", 
                               value="\n".join(st.session_state.project_years))
        if st.button("Update Project Years"):
            st.session_state.project_years = [y.strip() for y in years_text.split('\n') if y.strip()]
            save_data()
            st.experimental_rerun()
    
    with manage_tab2:
        st.subheader("Manage City Codes")
        cities_text = st.text_area("City Codes (one per line)", 
                               value="\n".join(st.session_state.city_codes))
        if st.button("Update City Codes"):
            st.session_state.city_codes = [c.strip() for c in cities_text.split('\n') if c.strip()]
            save_data()
            st.experimental_rerun()
    
    with manage_tab3:
        st.subheader("Manage Disciplines")
        disciplines_text = st.text_area("Disciplines (CODE: Description, one per line)", 
                                    value="\n".join([f"{k}: {v}" for k, v in st.session_state.disciplines.items()]))
        if st.button("Update Disciplines"):
            new_disciplines = {}
            for line in disciplines_text.split('\n'):
                if ':' in line and line.strip():
                    code, desc = line.split(':', 1)
                    new_disciplines[code.strip()] = desc.strip()
            st.session_state.disciplines = new_disciplines
            save_data()
            st.experimental_rerun()
    
    with manage_tab4:
        st.subheader("Manage Document Types")
        doc_types_text = st.text_area("Document Types (CODE: Description, one per line)", 
                                   value="\n".join([f"{k}: {v}" for k, v in st.session_state.doc_types.items()]))
        if st.button("Update Document Types"):
            new_doc_types = {}
            for line in doc_types_text.split('\n'):
                if ':' in line and line.strip():
                    code, desc = line.split(':', 1)
                    new_doc_types[code.strip()] = desc.strip()
            st.session_state.doc_types = new_doc_types
            save_data()
            st.experimental_rerun()
    
    with manage_tab5:
        st.subheader("Manage Elements")
        elements_text = st.text_area("Elements (CODE: Description, one per line)", 
                                  value="\n".join([f"{k}: {v}" for k, v in st.session_state.elements.items()]))
        if st.button("Update Elements"):
            new_elements = {}
            for line in elements_text.split('\n'):
                if ':' in line and line.strip():
                    code, desc = line.split(':', 1)
                    new_elements[code.strip()] = desc.strip()
            st.session_state.elements = new_elements
            save_data()
            st.experimental_rerun()
    
    with manage_tab6:
        st.subheader("Manage Companies")
        companies_text = st.text_area("Companies (CODE: Name, one per line)", 
                                   value="\n".join([f"{k}: {v}" for k, v in st.session_state.companies.items()]))
        if st.button("Update Companies"):
            new_companies = {}
            for line in companies_text.split('\n'):
                if ':' in line and line.strip():
                    code, name = line.split(':', 1)
                    new_companies[code.strip()] = name.strip()
            st.session_state.companies = new_companies
            save_data()
            st.experimental_rerun()
    
    # Export/Import Section
    st.subheader("Export/Import Data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export All Data"):
            export_data = {
                'project_years': st.session_state.project_years,
                'city_codes': st.session_state.city_codes,
                'disciplines': st.session_state.disciplines,
                'doc_types': st.session_state.doc_types,
                'elements': st.session_state.elements,
                'revisions': st.session_state.revisions,
                'file_extensions': st.session_state.file_extensions,
                'companies': st.session_state.companies,
                'letter_registry': st.session_state.letter_registry
            }
            st.download_button(
                label="Download Data",
                data=json.dumps(export_data, indent=4),
                file_name="filename_generator_export.json",
                mime="application/json",
            )
    
    with col2:
        uploaded_file = st.file_uploader("Import Data", type=['json'])
        if uploaded_file is not None:
            try:
                import_data = json.load(uploaded_file)
                st.session_state.project_years = import_data.get('project_years', st.session_state.project_years)
                st.session_state.city_codes = import_data.get('city_codes', st.session_state.city_codes)
                st.session_state.disciplines = import_data.get('disciplines', st.session_state.disciplines)
                st.session_state.doc_types = import_data.get('doc_types', st.session_state.doc_types)
                st.session_state.elements = import_data.get('elements', st.session_state.elements)
                st.session_state.revisions = import_data.get('revisions', st.session_state.revisions)
                st.session_state.file_extensions = import_data.get('file_extensions', st.session_state.file_extensions)
                st.session_state.companies = import_data.get('companies', st.session_state.companies)
                st.session_state.letter_registry = import_data.get('letter_registry', st.session_state.letter_registry)
                save_data()
                st.success("Data imported successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error importing data: {e}")

with tab4:
    st.header("Help & Reference")
    
    with st.expander("Naming Convention"):
        st.markdown("""
        ### Filename Format
        `[Project Year]-[City][Project Number]-[Discipline]-[Doc Type]-[Element]-[Revision].[Extension]`
        
        ### Example
        `CE24-CAI1-STR-D-WTP-A.pdf` represents:
        - A 2024 Construction Engineering project
        - Located in Cairo (project #1)
        - Structural discipline
        - Drawing document
        - For Water Treatment Plant
        - Revision A
        - PDF format
        """)
    
    with st.expander("Letter Management"):
        st.markdown("""
        ### Letter Documents
        
        When creating documents with type "LTR" (Letter), additional information is collected:
        
        1. **Direction**: Whether the letter is incoming (received) or outgoing (sent)
        2. **Company**: The external company involved in the correspondence
        3. **Subject**: Brief description of the letter's content
        4. **Attachments**: Any files attached to the letter
        
        All letters are automatically added to the Letter Registry for tracking and management.
        
        ### Letter Registry
        
        The Letter Registry allows you to:
        - View all correspondence in one place
        - Filter letters by direction, company, or attachment status
        - Sort letters by date or company
        - View attachment details
        """)
    
    with st.expander("Data Management"):
        st.markdown("""
        ### Managing Lookup Data
        
        The Data Management tab allows you to:
        
        1. **Add/Remove Options**: Modify the available options for dropdowns
        2. **Export Data**: Save all settings and the letter registry to a JSON file
        3. **Import Data**: Load settings from a previously exported file
        
        All changes are automatically saved and will persist between sessions.
        """)
    
    with st.expander("City Codes"):
        city_names = ["Beni Suef", "Sohag", "Cairo", "Giza", "Alexandria", "Sharm El Sheikh", "Luxor", 
                   "Aswan", "Ismailia", "Fayoum", "El Sharqia", "Assiut", "El Minya", "Zagazig", 
                   "Port Said", "Port Tawfik", "Qena", "Suez", "El Menia", "Damietta", "Dakahlia", 
                   "Monufia", "Qalubiya", "Kafr El Sheikh", "Matrouh", "Red Sea", "El Sharkia", 
                   "6th of October", "Ramadan", "New Cairo"]
        
        city_df = []
        for i, code in enumerate(st.session_state.city_codes):
            if i < len(city_names):
                city_df.append({"Code": code, "City": city_names[i]})
            else:
                city_df.append({"Code": code, "City": "Unknown"})
        st.table(city_df)
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("Disciplines"):
            disciplines_df = [{"Code": k, "Description": v} for k, v in st.session_state.disciplines.items()]
            st.table(disciplines_df)
        
        with st.expander("Document Types"):
            doc_types_df = [{"Code": k, "Description": v} for k, v in st.session_state.doc_types.items()]
            st.table(doc_types_df)
        
        with st.expander("Companies"):
            companies_df = [{"Code": k, "Name": v} for k, v in st.session_state.companies.items()]
            st.table(companies_df)
    
    with col2:
        with st.expander("Elements"):
            elements_df = [{"Code": k, "Description": v} for k, v in st.session_state.elements.items()]
            st.table(elements_df)
        
        with st.expander("Tips"):
            st.markdown("""
            - Use consistent naming conventions across all projects
            - Always include the revision letter even for first versions
            - Update the revision when making significant changes
            - Include the date in metadata for version tracking
            - For letters, maintain clear subject lines for easier searching
            - Regularly export data as a backup
            """)

# Footer
st.divider()
st.caption("Document Filename Generator © 2025")