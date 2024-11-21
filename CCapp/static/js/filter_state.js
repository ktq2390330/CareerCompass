// document.addEventListener('DOMContentLoaded', () => {
//     const pageID = (() => {
//         const path = window.location.pathname;
//         if (path.includes('filter_area')) return 'filter_area';
//         if (path.includes('filter_industry')) return 'filter_industry';
//         if (path.includes('filter_jobtype')) return 'filter_jobtype';
//         if (path.includes('filter_benefits')) return 'filter_benefits';
//         return 'default';
//     })();

//     function saveFilterState(filterState) {
//         // クッキーに保存
//         const filterStateJSON = JSON.stringify(filterState);
//         document.cookie = `filterStates_${pageID}=${encodeURIComponent(filterStateJSON)}; path=/;`;
//     }

//     function loadFilterState() {
//         const cookies = document.cookie.split(';');
//         let filterState = {};
//         cookies.forEach(cookie => {
//             const [name, value] = cookie.split('=').map(c => c.trim());
//             if (name === `filterStates_${pageID}`) {
//                 filterState = JSON.parse(decodeURIComponent(value));
//             }
//         });
//         console.log('Loaded Filter States from cookies:', filterState);
//         return filterState || {};
//     }

//     function saveCheckboxState() {
//         const filterState = {};
//         document.querySelectorAll('input[type="checkbox"][name="area[]"]').forEach(checkbox => {
//             const value = checkbox.value; // valueをキーとして利用
//             filterState[value] = checkbox.checked || false;
//         });
//         console.log('Saving Filter State for Page:', pageID, filterState);
//         saveFilterState(filterState);
//     }

//     function restoreCheckboxState() {
//         const filterState = loadFilterState();
//         console.log('Restoring Filter State for Page:', pageID, filterState);
//         document.querySelectorAll('input[type="checkbox"][name="area[]"]').forEach(checkbox => {
//             const value = checkbox.value;
//             if (filterState.hasOwnProperty(value)) {
//                 checkbox.checked = !!filterState[value];
//                 console.log(`Checkbox with value=${value}: Restored to ${checkbox.checked}`);
//             }
//         });
//     }

//     restoreCheckboxState();

//     document.querySelectorAll('input[type="checkbox"][name="area[]"]').forEach(checkbox => {
//         checkbox.addEventListener('change', saveCheckboxState);
//         console.log('Checkbox Event Attached:', checkbox.value);
//     });
// });
