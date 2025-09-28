import { jsx as _jsx } from "react/jsx-runtime";
import { BaseLayout } from './layout/BaseLayout';
import { GameProvider } from './contexts/GameContext';
function App() {
    return (_jsx(GameProvider, { children: _jsx(BaseLayout, {}) }));

}
export default App;
