using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace mxAutomation_wpf
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            //MainViewModel mainViewModel = new MainViewModel();
            //DataContext = mainViewModel;
            
        }

        public MainViewModel ViewModel => (MainViewModel) DataContext;

        private void A1_X_Plus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.X_A1_Plus = true;
        }

        private void A1_X_Plus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.X_A1_Plus = false;
        }

        private void A1_X_Minus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.X_A1_Minus = true;
        }

        private void A1_X_Minus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.X_A1_Minus = false;
        }

        private void A2_Y_Plus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.Y_A2_Plus = true;
        }

        private void A2_Y_Plus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.Y_A2_Plus = false;
        }

        private void A2_Y_Minus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.Y_A2_Minus = true;
        }

        private void A2_Y_Minus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.Y_A2_Minus = false;
        }

        private void A3_Z_Plus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.Z_A3_Plus = true;
        }

        private void A3_Z_Plus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.Z_A3_Plus = false;
        }

        private void A3_Z_Minus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.Z_A3_Minus = true;
        }

        private void A3_Z_Minus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.Z_A3_Minus = false;
        }

        private void A4_A_Plus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.A_A4_Plus = true;
        }

        private void A4_A_Plus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.A_A4_Plus = false;
        }

        private void A4_A_Minus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.A_A4_Minus = true;
        }

        private void A4_A_Minus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.A_A4_Minus = false;
        }

        private void A5_B_Plus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.B_A5_Plus = true;
        }

        private void A5_B_Plus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.B_A5_Plus = false;
        }

        private void A5_B_Minus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.B_A5_Minus = true;
        }

        private void A5_B_Minus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.B_A5_Minus = false;
        }

        private void A6_C_Plus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.C_A6_Plus = true;
        }

        private void A6_C_Plus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.C_A6_Plus = false;
        }

        private void A6_C_Minus_ButtonDown(object sender, MouseButtonEventArgs e)
        {
            ViewModel.C_A6_Minus = true;
        }

        private void A6_C_Minus_ButtonUp(object sender, MouseButtonEventArgs e)
        {
            ViewModel.C_A6_Minus = false;
        }

        private void LogBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            TextBox textBox = (TextBox)sender;
            textBox.ScrollToEnd();
        }
    }
}
