"""
Tooltip and info icon components for the UI.
"""

import tkinter as tk


class ToolTip:
    """Elegant tooltip class with delayed appearance."""
    
    def __init__(self, widget, text, delay=800):
        """
        Initialize tooltip.
        
        Args:
            widget: The widget to attach the tooltip to
            text: Text to display in the tooltip
            delay: Delay in milliseconds before showing tooltip
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self.show_timer = None
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)
    
    def on_enter(self, event=None):
        """Handle mouse enter event."""
        if self.show_timer:
            self.widget.after_cancel(self.show_timer)
        self.show_timer = self.widget.after(self.delay, self.show_tooltip)
    
    def on_leave(self, event=None):
        """Handle mouse leave event."""
        if self.show_timer:
            self.widget.after_cancel(self.show_timer)
            self.show_timer = None
        self.hide_tooltip()
    
    def on_motion(self, event=None):
        """Handle mouse motion event."""
        if self.tooltip_window:
            self.hide_tooltip()
    
    def show_tooltip(self, event=None):
        """Show the tooltip window."""
        if self.tooltip_window or not self.text:
            return
        
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + self.widget.winfo_height() // 2
        
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        # Add a subtle shadow effect
        shadow = tk.Frame(tw, background='#888888')
        shadow.pack(padx=(2, 0), pady=(2, 0))
        
        content = tk.Frame(shadow, background="#fffef0", relief=tk.SOLID, borderwidth=1)
        content.pack()
        
        label = tk.Label(content, text=self.text, justify=tk.LEFT,
                        background="#fffef0", foreground="#333333",
                        font=("Segoe UI", 9), wraplength=300, padx=8, pady=6)
        label.pack()
        
        # Fade in effect (simplified)
        tw.attributes('-alpha', 0.9)
    
    def hide_tooltip(self, event=None):
        """Hide the tooltip window."""
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()


class InfoIcon:
    """Small info icon that shows tooltip on hover."""
    
    def __init__(self, parent, tooltip_text, delay=500):
        """
        Initialize info icon.
        
        Args:
            parent: Parent widget
            tooltip_text: Text to show in tooltip
            delay: Delay before showing tooltip
        """
        self.icon = tk.Label(parent, text="ⓘ", font=("Segoe UI", 10), 
                           foreground="#666666", cursor="question_arrow",
                           padx=2, pady=0)
        self.tooltip = ToolTip(self.icon, tooltip_text, delay)
    
    def grid(self, **kwargs):
        """Grid the icon widget."""
        self.icon.grid(**kwargs)
    
    def pack(self, **kwargs):
        """Pack the icon widget."""
        self.icon.pack(**kwargs)
