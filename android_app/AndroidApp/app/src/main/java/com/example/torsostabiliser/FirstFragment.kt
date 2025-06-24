package com.example.torsostabiliser

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.findNavController
import com.example.torsostabiliser.databinding.FragmentFirstBinding
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.bluetooth.le.ScanCallback
import android.bluetooth.le.ScanResult
import android.widget.ArrayAdapter
import android.widget.ListView
import android.content.Context
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat
import android.Manifest
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothGatt
import android.bluetooth.BluetoothGattCallback
import android.bluetooth.BluetoothGattCharacteristic
import android.bluetooth.BluetoothGattDescriptor
import android.bluetooth.BluetoothProfile
import android.widget.SeekBar
import android.widget.TextView
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.util.UUID

class FirstFragment : Fragment() {

    private var _binding: FragmentFirstBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    private lateinit var bluetoothAdapter: BluetoothAdapter

    private val PERMISSION_REQUEST_FINE_LOCATION = 1

    private val targetDeviceName = "Torso Stabiliser"
    private val targetDeviceAddress = "F4:12:FA:59:97:DD"

    private val serviceUUID = UUID.fromString("A07498CA-AD5B-474E-940D-16F1FBE7E8CD")
    private val thresholdCharacteristicUUID = UUID.fromString("51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B")
    private val statusCharacteristicUUID = UUID.fromString("54855A27-E740-479B-B202-95ED22B1D437")
    private val releaseTimeCharacteristicUUID = UUID.fromString("30DDCD11-45FC-4A90-BD3D-83C969F48ADF")
    private var bluetoothGatt: BluetoothGatt? = null

    private lateinit var thresholdSlider: SeekBar
    private lateinit var thresholdSliderValueTextView: TextView

    private lateinit var releaseTimeSlider: SeekBar
    private lateinit var releaseTimeSliderValueTextView: TextView

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentFirstBinding.inflate(inflater, container, false)

        // Initialize Bluetooth adapter
        val bluetoothManager = requireContext().getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        bluetoothAdapter = bluetoothManager.adapter

        checkPermissions()

        return binding.root

    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        thresholdSlider = view.findViewById(R.id.thresholdSlider)
        thresholdSliderValueTextView = view.findViewById(R.id.thresholdSliderValue)

        thresholdSlider.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                // Optionally update a TextView to show the value while sliding
                val scaledValue = progress / 10.0f // Scale the value
                thresholdSliderValueTextView.text = "Threshold: ${String.format("%.1f", scaledValue)}"

            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
                // Optional, implement if needed
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
                seekBar?.let {
                    val scaledValue = it.progress / 10.0f // Scale the value
                    sendSliderValueToBLEDevice(scaledValue, thresholdCharacteristicUUID)
                }
            }
        })

        releaseTimeSlider = view.findViewById(R.id.releaseTimeSlider)
        releaseTimeSliderValueTextView = view.findViewById(R.id.releaseTimeValue)

        releaseTimeSlider.max = 25

        releaseTimeSlider.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                // Optionally update a TextView to show the value while sliding
                val scaledValue = progress + 5.0// Scale the value
                releaseTimeSliderValueTextView.text = "Release Time: ${String.format("%.1f", scaledValue)}"

            }

            override fun onStartTrackingTouch(seekBar: SeekBar?) {
                // Optional, implement if needed
            }

            override fun onStopTrackingTouch(seekBar: SeekBar?) {
                seekBar?.let {
                    val scaledValue = it.progress + 5.0// Scale the value
                    sendSliderValueToBLEDevice(scaledValue.toFloat(), releaseTimeCharacteristicUUID)
                }
            }
        })

        updateCircleColorConnection(false)

        binding.scanButton.setOnClickListener {
            startScan()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    private fun startScan() {
        val scanCallback = object : ScanCallback() {
            override fun onScanResult(callbackType: Int, result: ScanResult) {
                val deviceName = result.device.name ?: "Unknown Device"
                val deviceAddress = result.device.address

                if (deviceAddress == targetDeviceAddress) {
                    bluetoothAdapter.bluetoothLeScanner.stopScan(this) // Stop scanning
                    connectToDevice(result.device)
                }
            }
        }

        if (ContextCompat.checkSelfPermission(requireContext(),
                Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
            bluetoothAdapter.bluetoothLeScanner.startScan(scanCallback)
        } else {
            // Request permissions or handle the lack of permissions.
        }
    }

    private fun checkPermissions() {
        if (ContextCompat.checkSelfPermission(
                requireContext(),
                Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {

            requestPermissions(
                arrayOf(Manifest.permission.ACCESS_FINE_LOCATION),
                PERMISSION_REQUEST_FINE_LOCATION)
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int,
                                            permissions: Array<String>,
                                            grantResults: IntArray) {
        when (requestCode) {
            PERMISSION_REQUEST_FINE_LOCATION -> {
                if (grantResults.isEmpty() || grantResults[0] != PackageManager.PERMISSION_GRANTED) {
                    // Permission was denied, handle the case where the user denies the permission.
                } else {
                    // Permission was granted, you can start BLE scanning here if appropriate.
                }
            }
        }
    }

    private fun showSlider() {
        activity?.runOnUiThread {
            thresholdSlider.visibility = View.VISIBLE
        }
    }

    private fun connectToDevice(device: BluetoothDevice) {
        bluetoothGatt = device.connectGatt(context, false, gattCallback)
    }

    private val gattCallback = object : BluetoothGattCallback() {
        override fun onConnectionStateChange(gatt: BluetoothGatt, status: Int, newState: Int) {
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                // Discover services after successful connection
                gatt.discoverServices()
            }
            // Handle other connection states (e.g., disconnected)
        }

        override fun onServicesDiscovered(gatt: BluetoothGatt, status: Int) {
            if (status == BluetoothGatt.GATT_SUCCESS) {

                //showSlider() // Show the slider now that the device is connected
                updateCircleColorConnection(true)

                val service = gatt.getService(serviceUUID)
                val statusCharacteristic = service.getCharacteristic(statusCharacteristicUUID)
                gatt.setCharacteristicNotification(statusCharacteristic, true)
                // Set up descriptor to enable notification/indication
                val descriptor = statusCharacteristic.getDescriptor(
                    UUID.fromString("00002902-0000-1000-8000-00805f9b34fb")
                )
                descriptor.value = BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE
                gatt.writeDescriptor(descriptor)


            }
        }

        override fun onCharacteristicChanged(gatt: BluetoothGatt, characteristic: BluetoothGattCharacteristic) {
            if (characteristic.uuid == statusCharacteristicUUID) {
                val status = characteristic.getIntValue(BluetoothGattCharacteristic.FORMAT_UINT8, 0)
                updateCircleColor(status == 1)
            }
        }

        // ... other callback methods like onCharacteristicRead, onCharacteristicWrite, etc ...
    }

    private fun sendSliderValueToBLEDevice(value: Float, characteristicUUID: UUID) {
        val service = bluetoothGatt?.getService(serviceUUID)
        val characteristic = service?.getCharacteristic(characteristicUUID)

        characteristic?.let {
            it.writeType = BluetoothGattCharacteristic.WRITE_TYPE_DEFAULT
            val buffer = ByteBuffer.allocate(4).order(ByteOrder.LITTLE_ENDIAN).putFloat(value).array()
            it.value = buffer
            bluetoothGatt?.writeCharacteristic(it)
        }
    }

    private fun updateCircleColor(isExtended: Boolean) {
        val color = if (isExtended) R.color.red else R.color.green
        activity?.runOnUiThread {
            binding.statusCircle.setBackgroundColor(ContextCompat.getColor(requireContext(), color))
        }
    }

    private fun updateCircleColorConnection(isConnected: Boolean) {
        val color = if (isConnected) R.color.green else R.color.black
        activity?.runOnUiThread {
            binding.statusCircle.setBackgroundColor(ContextCompat.getColor(requireContext(), color))
        }
    }

}